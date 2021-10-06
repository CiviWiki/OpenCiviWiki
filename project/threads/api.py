import json
import PIL
import urllib

from notifications.signals import notify
from accounts.models import Profile
from core.custom_decorators import require_post_params
from django.core.files import File
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .models import CiviImage
from django.db.models.query import F
from django.contrib.auth import get_user_model
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseServerError,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)

from .models import Activity, Civi, Thread
from .utils import json_response
from core.constants import US_STATES


@login_required
@require_post_params(params=["title", "summary", "category_id"])
def new_thread(request):
    """
    USAGE:
        Use this function when a user creates a new thread.

    Data needed to create new thread:
        - Title, Summary, Category, Author, Level, State
    """
    try:
        author = request.user
        new_thread_data = dict(
            title=request.POST["title"],
            summary=request.POST["summary"],
            category_id=request.POST["category_id"],
            author=author,
            level=request.POST["level"],
        )
        state = request.POST["state"]
        if state:
            new_thread_data["state"] = state

        new_t = Thread(**new_thread_data)
        new_t.save()

        return JsonResponse({"data": "success", "thread_id": new_t.pk})
    except Profile.DoesNotExist:
        return HttpResponseServerError(reason=f"Profile with user:{request.user.username} does not exist")
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


def get_thread(request, thread_id):
    """
    USAGE:
       This is used to get a requested thread
    """
    try:
        t = Thread.objects.get(id=thread_id)
        civis = Civi.objects.filter(thread_id=thread_id)
        requested_user = request.user

        # TODO: move order by to frontend or accept optional arg
        c = civis.order_by("-created")
        c_scores = [ci.score(requested_user.id) for ci in c]
        c_data = [Civi.objects.serialize_s(ci) for ci in c]

        problems = []
        for idx, item in enumerate(c_data):
            problems[idx]["score"] = c_scores[idx]

        data = {
            "title": t.title,
            "summary": t.summary,
            "tags": t.tags.all().values(),
            "author": {
                "username": t.author.username,
                "profile_image": t.author.profile.profile_image.url
                if t.author.profile.profile_image
                else "/media/profile/default.png",
                "first_name": t.author.first_name,
                "last_name": t.author.last_name,
            },
            "category": model_to_dict(t.category),
            "created": t.created,
            "contributors": [
                Profile.objects.chip_summarize(u.profile)
                for u in get_user_model().objects.filter(
                    pk__in=civis.distinct("author").values_list("author", flat=True)
                )
            ],
            "num_civis": t.num_civis,
            "num_views": t.num_views,
            "votes": [
                {
                    "civi_id": act.civi.id,
                    "activity_type": act.activity_type,
                    "user": act.user.id,
                }
                for act in Activity.objects.filter(thread=t.id, user=requested_user.id)
            ],
        }

        # modify thread view count
        t.num_views = t.num_views + 1
        t.save()

        return json_response(data)
    except Thread.DoesNotExist:
        return HttpResponseBadRequest(reason=f"Thread with id:{thread_id} does not exist")
    except Profile.DoesNotExist:
        return HttpResponseBadRequest(reason=f"Profile with username:{request.user.username} does not exist")
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))


def get_civi(request, civi_id):
    """
    USAGE:
       This is used to get a specified Civi
    """
    try:
        c = Civi.objects.serialize(Civi.objects.get(id=civi_id))
        return JsonResponse(c, safe=False)
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))


def get_civis(request, thread_id):
    """
    USAGE:
       This is used ot get a group of specified Civis
    """
    try:
        c = [Civi.objects.serialize(c) for c in Civi.objects.filter(thread=thread_id)]
        return JsonResponse(c)
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))


def get_responses(request, thread_id, civi_id):
    """
    USAGE:
       This is used to get responses for a Civi
    """
    try:
        requested_user = request.user
        c_qs = Civi.objects.get(id=civi_id).responses.all()
        c_scored = []
        for res_civi in c_qs:
            c_dict = res_civi.dict_with_score(requested_user.id)
            c_rebuttal = res_civi.responses.all()
            if c_rebuttal:
                c_dict["rebuttal"] = c_rebuttal[0].dict_with_score(requested_user.id)
            c_scored.append(c_dict)

        civis = sorted(c_scored, key=lambda c: c["score"], reverse=True)

        return JsonResponse(civis, safe=False)
    except Profile.DoesNotExist:
        return HttpResponseBadRequest(reason=f"Profile with user:{request.user.username} does not exist")
    except Civi.DoesNotExist:
        return HttpResponseBadRequest(reason=f"Civi with id:{civi_id} does not exist")
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))


@login_required
@require_post_params(params=["title", "body", "c_type", "thread_id"])
def create_civi(request):
    """
    USAGE:
        Use this function to insert a new connected civi into the database.

    :return: (200, ok) (400, missing required parameter) (500, internal error)
    """

    user = request.user
    thread_id = request.POST.get("thread_id")
    data = {
        "author": request.user,
        "title": request.POST.get("title", ""),
        "body": request.POST.get("body", ""),
        "c_type": request.POST.get("c_type", ""),
        "thread": Thread.objects.get(id=thread_id),
    }

    try:
        civi = Civi(**data)
        civi.save()
        links = request.POST.getlist("links[]", "")
        if links:
            for civi_id in links:
                linked_civi = Civi.objects.get(id=civi_id)
                civi.linked_civis.add(linked_civi)

        # If response
        related_civi = request.POST.get("related_civi", "")
        if related_civi:
            parent_civi = Civi.objects.get(id=related_civi)
            parent_civi.responses.add(civi)

            if parent_civi.author.username != request.user.username:
                notify.send(
                    request.user,  # Actor User
                    recipient=parent_civi.author,  # Target User
                    verb=u"responded to your civi",  # Verb
                    action_object=civi,  # Action Object
                    target=civi.thread,  # Target Object
                    popup_string="{user} responded to your civi in {thread}".format(
                        user=user.full_name, thread=civi.thread.title
                    ),
                    link="/{}/{}".format("thread", thread_id),
                )

        else:  # not a reply, a regular civi
            c_qs = Civi.objects.filter(thread_id=thread_id)
            users = get_user_model().objects.filter(
                pk__in=c_qs.values("author").distinct()
            )
            data = {
                "command": "add",
                "data": json.dumps(civi.dict_with_score(user.id)),
            }

            for u in users:
                if u.username != request.user.username:
                    notify.send(
                        request.user,  # Actor User
                        recipient=u.user,  # Target User
                        verb=u"created a new civi",  # Verb
                        action_object=civi,  # Action Object
                        target=civi.thread,  # Target Object
                        popup_string="{user} created a new civi in the thread {thread}".format(
                            user=user.full_name, thread=civi.thread.title
                        ),
                        link="/{}/{}".format("thread", thread_id),
                    )

        return JsonResponse({"data": civi.dict_with_score(user.id)})
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
@require_post_params(params=["civi_id", "rating"])
def rate_civi(request):
    """ Use this function to rate a Civi """
    civi_id = request.POST.get("civi_id", "")
    rating = request.POST.get("rating", "")
    user = request.user

    voted_civi = Civi.objects.get(id=civi_id)

    if voted_civi.thread.is_draft:
        return HttpResponseServerError(
            reason=str("Cannot vote on a civi that is in a thread still in draft mode")
        )

    try:
        prev_act = Activity.objects.get(civi=voted_civi, user=user)
    except Activity.DoesNotExist:
        prev_act = None

    activity_data = {
        "user": user,
        "thread": voted_civi.thread,
        "civi": voted_civi,
    }

    activity_vote_key = "votes_{}".format(rating)
    vote_val = "vote_{}".format(rating)
    # F object doesn't cause losing data in case of race
    setattr(voted_civi, activity_vote_key, F(activity_vote_key) + 1)
    voted_civi.save()

    if prev_act:
        prev_act.activity_type = vote_val
        prev_act.save()
        act = prev_act
    else:
        act = Activity(**activity_data)
        act.save()

    data = {
        "civi_id": act.civi.id,
        "activity_type": act.activity_type,
        "c_type": act.civi.c_type,
    }
    return JsonResponse({"data": data})


@login_required
def edit_civi(request):
    """ Use this function to edit an existing Civi"""
    civi_id = request.POST.get("civi_id", "")
    title = request.POST.get("title", "")
    body = request.POST.get("body", "")
    civi_type = request.POST.get("type", "")

    c = Civi.objects.get(id=civi_id)
    if request.user.username != c.author.username:
        return HttpResponseBadRequest(reason="No Edit Rights")

    try:
        c.title = title
        c.body = body
        c.c_type = civi_type
        c.save(update_fields=["title", "body"])

        links = request.POST.getlist("links[]", "")
        c.linked_civis.clear()
        if links:
            for civiimage_id in links:
                linked_civi = Civi.objects.get(id=civiimage_id)
                c.linked_civis.add(linked_civi)

        image_remove_list = request.POST.getlist("image_remove_list[]", "")
        if image_remove_list:
            for image_id in image_remove_list:
                civi_image = CiviImage.objects.get(id=image_id)
                civi_image.delete()

        return JsonResponse(c.dict_with_score(request.user.id))
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
def delete_civi(request):
    """ Use this function to delete an existing Civi """
    civi_id = request.POST.get("civi_id", "")

    c = Civi.objects.get(id=civi_id)
    if request.user.username != c.author.username:
        return HttpResponseBadRequest(reason="No Edit Rights")

    try:
        c.delete()

        return HttpResponse("Success")
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
def edit_thread(request):
    """ Use this function to edit an existing thread """
    thread_id = request.POST.get("thread_id")
    non_required_params = ["title", "summary", "category_id", "level", "state"]
    is_draft = request.POST.get("is_draft", True)

    if not thread_id:
        return HttpResponseBadRequest(reason="Invalid Thread Reference")

    # for some reason this is not cast to boolean in the request
    if is_draft == "false":
        Thread.objects.filter(id=thread_id).update(is_draft=False)

        return JsonResponse({"data": "Success"})

    try:
        req_edit_thread = Thread.objects.get(id=thread_id)

        if request.user.username != req_edit_thread.author.username:
            return HttpResponseBadRequest("No Edit Rights")

        # set remaining parameters from request
        for param in non_required_params:
            request_value = request.POST.get(param)

            if request_value:
                setattr(req_edit_thread, param, request_value)

        req_edit_thread.save()
    except Thread.DoesNotExist:
        return HttpResponseServerError(reason=f"Thread with id:{thread_id} does not exist")
    except Exception as e:
        return HttpResponseServerError(reason=str(e))

    location = (
        req_edit_thread.level
        if not req_edit_thread.state
        else dict(US_STATES).get(req_edit_thread.state)
    )

    return_data = {
        "thread_id": thread_id,
        "title": req_edit_thread.title,
        "summary": req_edit_thread.summary,
        "category": {
            "id": req_edit_thread.category.id,
            "name": req_edit_thread.category.name,
        },
        "level": req_edit_thread.level,
        "state": req_edit_thread.state if req_edit_thread.level == "state" else "",
        "location": location,
    }
    return JsonResponse({"data": return_data})


@login_required
def upload_civi_image(request):
    """This function is used to upload an image for a Civi"""
    if request.method == "POST":
        r = request.POST
        civi_id = r.get("civi_id")
        if not civi_id:
            return HttpResponseBadRequest(reason="Invalid Civi Reference")

        try:
            c = Civi.objects.get(id=civi_id)

            attachment_links = request.POST.getlist("attachment_links[]")

            if attachment_links:
                for img_link in attachment_links:
                    result = urllib.urlretrieve(img_link)
                    img_file = File(open(result[0]))
                    if check_image_with_pil(img_file):
                        civi_image = CiviImage(title="", civi=c, image=img_file)
                        civi_image.save()

            if len(request.FILES) != 0:
                for image in request.FILES.getlist("attachment_image"):
                    civi_image = CiviImage(title="", civi=c, image=image)
                    civi_image.save()

            data = {
                "attachments": [
                    {"id": img.id, "image_url": img.image_url} for img in c.images.all()
                ],
            }
            return JsonResponse(data)

        except Civi.DoesNotExist:
            return HttpResponseServerError(reason=f"Civi with id:{civi_id} does not exist")
        except Exception as e:
            return HttpResponseServerError(
                reason=(str(e) + civi_id + str(request.FILES))
            )
    else:
        return HttpResponseForbidden("allowed only via POST")


def check_image_with_pil(image_file):
    """This function uses the PIL library to make sure the image format is supported"""
    try:
        PIL.Image.open(image_file)
    except IOError:
        return False
    return True


@login_required
def upload_thread_image(request):
    """This function is used to upload an image to a thread"""
    if request.method == "POST":
        r = request.POST
        thread_id = r.get("thread_id")
        if not thread_id:
            return HttpResponseBadRequest(reason="Invalid Thread Reference")

        try:
            thread = Thread.objects.get(id=thread_id)
            remove = r.get("remove", "")
            img_link = r.get("link", "")
            if remove:
                thread.image.delete()
                thread.save()

            elif img_link:
                thread.image.delete()
                result = urllib.urlretrieve(img_link)
                img_file = File(open(result[0]))
                if check_image_with_pil(img_file):
                    thread.image = img_file
                    thread.save()
                # else:
                #     return HttpResponseBadRequest("Invalid Image")
            else:
                # Clean up previous image
                thread.image.delete()

                # Upload new image and set as profile picture
                thread.image = request.FILES["attachment_image"]
                thread.save()

            data = {"image": thread.image_url}
            return JsonResponse(data)

        except Thread.DoesNotExist:
            return HttpResponseServerError(reason=f"Thread with id:{thread_id} does not exist")
        except Exception as e:
            return HttpResponseServerError(reason=(str(e)))
    else:
        return HttpResponseForbidden("allowed only via POST")
