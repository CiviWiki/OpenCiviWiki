import json
import PIL
import urllib
import uuid

from notifications.signals import notify

# django packages
from django.db.models.query import F
from django.contrib.auth.models import User
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
from api.tasks import send_mass_email
from models import Account, Activity, Category, Civi, CiviImage, Invitation, Bill
from core.custom_decorators import require_post_params
from core.constants import US_STATES


@login_required
@require_post_params(params=["title", "summary", "category_id"])
def new_thread(request):
    new_thread_data = dict(
        title=request.POST["title"],
        summary=request.POST["summary"],
        category_id=request.POST["category_id"],
        author_id=request.user.id,
        level=request.POST["level"],
    )
    state = request.POST["state"]
    if state:
        new_thread_data["state"] = state

    new_t = Thread(**new_thread_data)
    new_t.save()

    return JsonResponse({"data": "success", "thread_id": new_t.pk})


@login_required
@require_post_params(params=["title", "body", "c_type", "thread_id"])
def createCivi(request):
    """
    USAGE:
        use this function to insert a new connected civi into the database.

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
        bills = request.POST.getlist("bills[]", "")
        if links:
            for civi_id in links:
                linked_civi = Civi.objects.get(id=civi_id)
                civi.linked_civis.add(linked_civi)

        if bills:
            for bill_id in bills:
                linked_bill = Bill.objects.get(id=bill_id)
                civi.linked_bills.add(linked_bill)

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
                pk__in=c_qs.distinct("author").values_list("author", flat=True)
            )
            data = {"command": "add", "data": json.dumps(civi.dict_with_score(a.id))}

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
    civi_id = request.POST.get("civi_id", "")

    c = Civi.objects.get(id=civi_id)
    if request.user.username != c.author.user.username:
        return HttpResponseBadRequest(reason="No Edit Rights")

    try:
        c.delete()

        return HttpResponse("Success")
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


# TODO 1: profile image file upload
# TODO 2: redo user editing
# TODO 3: django forms
# @login_required
# def get_dist(request):
#     '''
#     Upon First registering or changing location information gets representative codes and addes them to the user array
#     '''
#     request = urllib2.Request("https://congress.api.sunlightfoundation.com/")
#
#     #S3tting the key as the value of an X-APIKEY HTTP request header.
#     data = {
#     "apikey": APIKEY,
#     "fields": [],
#
#     }
#     request.add_data(json.dumps(data))
#
#     response = urllib2.urlopen(request)
#     resp_parsed = json.loads(response.read())
#     reps = [for rep in resp_parsed.data]
#     Account.user(request.user).representatives = reps
#


@login_required
def editThread(request):

    thread_id = request.POST.get("thread_id")
    non_required_params = ['title', 'summary', 'category_id', 'level', 'state']

    if not thread_id:
        return HttpResponseBadRequest(reason="Invalid Thread Reference")
    else:
        try:
            req_edit_thread = Thread.objects.get(id=thread_id)

            if request.user.username != req_edit_thread.author.user.username:
                return HttpResponseBadRequest("No Edit Rights")

            for param in non_required_params:
                request_value = request.POST.get(param)
                if request_value:
                    setattr(req_edit_thread, param, request_value)
            req_edit_thread.save()
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
    pass


@login_required
def editUser(request):
    """
    Edit Account Model
    """
    request_data = request.POST
    user = request.user
    account = Account.objects.get(user=user)
    interests = request_data.get("interests", False)

    if interests:
        interests = list(interests)
    else:
        interests = account.interests

    data = {
        "first_name": request_data.get("first_name", account.first_name),
        "last_name": request_data.get("last_name", account.last_name),
        "about_me": request_data.get("about_me", account.about_me),
        "address": request_data.get("address", account.address),
        "city": request_data.get("city", account.city),
        "state": request_data.get("state", account.state),
        "zip_code": request_data.get("zip_code", account.zip_code),
        "longitude": request_data.get("longitude", account.longitude),
        "latitude": request_data.get("latitude", account.latitude),
        "country": request_data.get("country", account.country),
    }

    account.__dict__.update(data)

    try:
        account.save()
    except Exception as e:
        return HttpResponseServerError(reason=str(e))

    account.refresh_from_db()

    return JsonResponse(Account.objects.summarize(account))


@login_required
def uploadProfileImage(request):
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
    if request.method == "POST":
        try:
            account = Account.objects.get(user=request.user)

            # Clean up previous image
            account.profile_image.delete()
            account.save()

            return HttpResponse("Image Deleted")
        except Exception:
            return HttpResponseServerError(reason=str("default"))
    else:
        return HttpResponseForbidden("allowed only via POST")


@login_required
def uploadCiviImage(request):
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
                ]
            }
            return JsonResponse(data)

        except Exception as e:
            return HttpResponseServerError(
                reason=(str(e) + civi_id + str(request.FILES))
            )
    else:
        return HttpResponseForbidden("allowed only via POST")


def check_image_with_pil(image_file):
    try:
        PIL.Image.open(image_file)
    except IOError:
        return False
    return True


@login_required
def uploadThreadImage(request):
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
        account = Account.objects.get(user=request.user)
        target = User.objects.get(username=request.POST.get("target", -1))
        target_account = Account.objects.get(user=target)

        account.following.remove(target_account)
        account.save()
        target_account.followers.remove(account)
        target_account.save()
        return JsonResponse({"result": "Success"})
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


@login_required
@user_passes_test(lambda u: u.is_staff)
def invite(request):
    emails = request.POST.getlist("emailList[]", "")
    custom_message = request.POST.get("custom_message", "")

    if emails:
        user = User.objects.get(username=request.user.username)
        user_account = Account.objects.get(user=user)
        did_not_invite = []

        # TODO: Move this to string templates
        if custom_message:
            email_body = (
                "{host_name} has invited you to be part of CiviWiki Beta "
                "with the following message: {custom_message}"
            ).format(host_name=user_account.full_name, custom_message=custom_message)
        else:
            email_body = (
                "{host_name} has invited you to be part of CiviWiki Beta. "
                "Follow the link below to get registered."
            ).format(host_name=user_account.full_name)

        email_messages = []
        valid_emails = []
        for email in emails:
            if Invitation.objects.filter(invitee_email=email).exists():
                did_not_invite.append(email)
            else:
                valid_emails.append(email)
                verification_hash = uuid.uuid4().hex[:31]
                data = {
                    "host_user": user,
                    "invitee_email": email,
                    "verification_code": verification_hash,
                }

                domain = get_current_site(request).domain
                base_url = "http://{domain}/beta_register/{email}/{token}"
                url_with_code = base_url.format(
                    domain=domain, email=email, token=verification_hash
                )

                email_context = {
                    "title": "You're Invited to Join CiviWiki Beta",
                    "greeting": "You're Invited to Join CiviWiki Beta",
                    "body": email_body,
                    "link": url_with_code,
                    "recipient": [email],
                }
                email_messages.append(email_context)

                new_invitation = Invitation(**data)
                new_invitation.save()

        if email_messages:
            email_subject = "Invitation to CiviWiki"
            send_mass_email.delay(subject=email_subject, contexts=email_messages)

        if len(did_not_invite) == len(emails):
            response_data = {
                "message": "Invitations exist for submitted email(s). No new invitations sent",
                "error": "INVALID_EMAIL_DATA",
            }
            return JsonResponse(response_data, status=400)

        invitations = (
            Invitation.objects.filter_by_host(host_user=user)
            .order_by("-date_created")
            .all()
        )
        invitees = [invitation.summarize() for invitation in invitations]

        response_data = {"did_not_invite": did_not_invite, "invitees": invitees}
        return JsonResponse(response_data)

    else:
        # Return an 'invalid login' error message.
        response = {"message": "Invalid Email Data", "error": "INVALID_EMAIL_DATA"}
        return JsonResponse(response, status=400)
