import json
import PIL
import urllib
import uuid

from notifications.signals import notify

# django packages
from django.db.models.query import F
from django.contrib.auth import get_user_model
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseServerError,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)

from django.core.files import File  # need this for image file handling
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sites.shortcuts import get_current_site

# civi packages
from api.forms import UpdateProfileImage
from api.models import Thread
from accounts.utils import send_mass_email
from .models import Activity, Category, Civi, CiviImage
from accounts.models import Account
from core.custom_decorators import require_post_params
from core.constants import US_STATES

User = get_user_model()


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
        author = Account.objects.get(user=request.user)
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
    except Account.DoesNotExist:
        return HttpResponseServerError(reason=f"Account with user:{request.user.username} does not exist")
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
@require_post_params(params=["title", "body", "c_type", "thread_id"])
def createCivi(request):
    """
    USAGE:
        Use this function to insert a new connected civi into the database.

    :return: (200, ok) (400, missing required parameter) (500, internal error)
    """

    a = Account.objects.get(user=request.user)
    thread_id = request.POST.get("thread_id")
    data = {
        "author": Account.objects.get(user=request.user),
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

            if parent_civi.author.user.username != request.user.username:
                notify.send(
                    request.user,  # Actor User
                    recipient=parent_civi.author.user,  # Target User
                    verb=u"responded to your civi",  # Verb
                    action_object=civi,  # Action Object
                    target=civi.thread,  # Target Object
                    popup_string="{user} responded to your civi in {thread}".format(
                        user=a.full_name, thread=civi.thread.title
                    ),
                    link="/{}/{}".format("thread", thread_id),
                )

        else:  # not a reply, a regular civi
            c_qs = Civi.objects.filter(thread_id=thread_id)
            accounts = Account.objects.filter(
                pk__in=c_qs.values("author").distinct()
            )
            data = {
                "command": "add",
                "data": json.dumps(civi.dict_with_score(a.id)),
            }

            for act in accounts:
                if act.user.username != request.user.username:
                    notify.send(
                        request.user,  # Actor User
                        recipient=act.user,  # Target User
                        verb=u"created a new civi",  # Verb
                        action_object=civi,  # Action Object
                        target=civi.thread,  # Target Object
                        popup_string="{user} created a new civi in the thread {thread}".format(
                            user=a.full_name, thread=civi.thread.title
                        ),
                        link="/{}/{}".format("thread", thread_id),
                    )

        return JsonResponse({"data": civi.dict_with_score(a.id)})
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
@require_post_params(params=["civi_id", "rating"])
def rateCivi(request):
    """ Use this function to rate a Civi """
    civi_id = request.POST.get("civi_id", "")
    rating = request.POST.get("rating", "")
    account = Account.objects.get(user=request.user)

    voted_civi = Civi.objects.get(id=civi_id)

    if voted_civi.thread.is_draft:
        return HttpResponseServerError(
            reason=str("Cannot vote on a civi that is in a thread still in draft mode")
        )

    try:
        prev_act = Activity.objects.get(civi=voted_civi, account=account)
    except Activity.DoesNotExist:
        prev_act = None

    activity_data = {
        "account": account,
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
def editCivi(request):
    """ Use this function to edit an existing Civi"""
    civi_id = request.POST.get("civi_id", "")
    title = request.POST.get("title", "")
    body = request.POST.get("body", "")
    civi_type = request.POST.get("type", "")

    c = Civi.objects.get(id=civi_id)
    if request.user.username != c.author.user.username:
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

        a = Account.objects.get(user=request.user)
        return JsonResponse(c.dict_with_score(a.id))
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
def deleteCivi(request):
    """ Use this function to delete an existing Civi """
    civi_id = request.POST.get("civi_id", "")

    c = Civi.objects.get(id=civi_id)
    if request.user.username != c.author.user.username:
        return HttpResponseBadRequest(reason="No Edit Rights")

    try:
        c.delete()

        return HttpResponse("Success")
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
def editThread(request):
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

        if request.user.username != req_edit_thread.author.user.username:
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
def uploadphoto(request):
    """
        This function is a work in progress
        Eventually will be used to allow users to upload photos
    """
    pass


@login_required
def editUser(request):
    """
    Edit Account Model
    """
    request_data = request.POST
    user = request.user
    account = Account.objects.get(user=user)

    data = {
        "first_name": request_data.get("first_name", account.first_name),
        "last_name": request_data.get("last_name", account.last_name),
        "about_me": request_data.get("about_me", account.about_me),
    }

    account.__dict__.update(data)

    try:
        account.save()
    except Exception as e:
        # print('EXCEPTION THROWN HERE!! ')
        return HttpResponseServerError(reason=str(e))

        account.refresh_from_db()

    return JsonResponse(Account.objects.summarize(account))


@login_required
def uploadProfileImage(request):
    """ This function is used to allow users to upload profile photos """
    if request.method == "POST":
        form = UpdateProfileImage(request.POST, request.FILES)
        if form.is_valid():
            try:
                account = Account.objects.get(user=request.user)

                # Clean up previous image
                account.profile_image.delete()

                # Upload new image and set as profile picture
                account.profile_image = form.clean_profile_image()
                try:
                    account.save()
                except Exception as e:
                    response = {"message": str(e), "error": "MODEL_SAVE_ERROR"}
                    return JsonResponse(response, status=400)

                request.session["login_user_image"] = account.profile_image_thumb_url

                response = {"profile_image": account.profile_image_url}
                return JsonResponse(response, status=200)

            except Account.DoesNotExist:
                response = {"message": f"Account with user {request.user.username} does not exist",
                            "error": "ACCOUNT_ERROR"}
                return JsonResponse(response, status=400)
            except Exception as e:
                response = {"message": str(e), "error": "MODEL_ERROR"}
                return JsonResponse(response, status=400)
        else:
            response = {"message": form.errors["profile_image"], "error": "FORM_ERROR"}
            return JsonResponse(response, status=400)

    else:
        return HttpResponseForbidden("allowed only via POST")


@login_required
def clearProfileImage(request):
    """ This function is used to delete a profile image """
    if request.method == "POST":
        try:
            account = Account.objects.get(user=request.user)

            # Clean up previous image
            account.profile_image.delete()
            account.save()

            return HttpResponse("Image Deleted")
        except Account.DoesNotExist:
            return HttpResponseServerError(reason=f"Account with id:{request.user.username} does not exist")
        except Exception:
            return HttpResponseServerError(reason=str("default"))
    else:
        return HttpResponseForbidden("allowed only via POST")


@login_required
def uploadCiviImage(request):
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
def uploadThreadImage(request):
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


@login_required
@require_post_params(params=["target"])
def requestFollow(request):
    """
    USAGE:
        Takes in user_id from current friend_requests list and joins accounts as friends.
        Does not join accounts as friends unless the POST friend is a valid member of the friend request array.

    Text POST:
        friend

    :return: (200, okay, list of friend information) (400, bad lookup) (500, error)
    """
    if request.user.username == request.POST.get("target", -1):
        return HttpResponseBadRequest(reason="You cannot follow yourself, silly!")

    try:
        account = Account.objects.get(user=request.user)
        target = User.objects.get(username=request.POST.get("target", -1))
        target_account = Account.objects.get(user=target)

        account.following.add(target_account)
        account.save()
        target_account.followers.add(account)
        target_account.save()
        data = {"username": target.username, "follow_status": True}

        notify.send(
            request.user,  # Actor User
            recipient=target,  # Target User
            verb=u"is following you",  # Verb
            target=target_account,  # Target Object
            popup_string="{user} is now following you".format(user=account.full_name),
            link="/{}/{}".format("profile", request.user.username),
        )

        return JsonResponse({"result": data})
    except Account.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
@require_post_params(params=["target"])
def requestUnfollow(request):
    """
    USAGE:
        Takes in user_id from current friend_requests list and joins accounts as friends.
        Does not join accounts as friends unless the POST friend is a valid member of the friend request array.

    Text POST:
        friend

    :return: (200, okay, list of friend information) (400, bad lookup) (500, error)
    """
    try:
        username = request.POST.get("target")
        if username:
            account = Account.objects.get(user=request.user)
            target = User.objects.get(username=username)
            target_account = Account.objects.get(user=target)

            account.following.remove(target_account)
            account.save()
            target_account.followers.remove(account)
            target_account.save()
            return JsonResponse({"result": "Success"})
        return HttpResponseBadRequest(reason=f"username cannot be empty ")

    except User.DoesNotExist:
        return HttpResponseBadRequest(reason=f"User with username {username} does not exist")
    except Account.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
def editUserCategories(request):
    """
    USAGE:
        Edits list of categories for the user

    """
    try:
        account = Account.objects.get(user=request.user)
        categories = [int(i) for i in request.POST.getlist("categories[]")]
        account.categories.clear()
        for category in categories:
            account.categories.add(Category.objects.get(id=category))
            account.save()

        data = {
            "user_categories": list(account.categories.values_list("id", flat=True))
            or "all_categories"
        }
        return JsonResponse({"result": data})
    except Account.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseServerError(reason=str(e))
