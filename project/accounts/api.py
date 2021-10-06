from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseServerError,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from notifications.signals import notify

from accounts.permissions import IsProfileOwnerOrDuringRegistrationOrReadOnly
from accounts.serializers import ProfileSerializer, ProfileListSerializer
from accounts.forms import UpdateProfileImage
from accounts.utils import get_account
from threads.models import Thread, Civi, Activity
from accounts.models import Profile
from categories.models import Category
from threads.utils import json_response
from threads.serializers import ThreadSerializer, CiviSerializer
from categories.serializers import CategorySerializer
from core.custom_decorators import require_post_params


class ProfileViewSet(ModelViewSet):

    """
    REST API viewset for an Profile
    retrieve:
    Return the given user based a username.

    list:
    Return a list of all the existing users. Only with privileged access.
    """

    queryset = Profile.objects.all()
    lookup_field = "user__username"
    serializer_class = ProfileSerializer
    http_method_names = ["get", "head", "put", "patch"]
    permission_classes = (IsProfileOwnerOrDuringRegistrationOrReadOnly,)
    authentication_classes = ()

    def list(self, request):
        """ """
        if self.request.user.is_staff:
            accounts = Profile.objects.all()
        else:
            accounts = Profile.objects.filter(user=self.request.user)
        serializer = ProfileListSerializer(accounts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, user__username=None):
        """ """
        account = get_account(username=user__username)
        if self.request.user == account.user:
            serializer = ProfileSerializer(account)
        else:
            serializer = ProfileListSerializer(account)
        return Response(serializer.data)

    @action(detail=True)
    def civis(self, request, user__username=None):
        """
        Gets the civis of the selected account
        /accounts/{username}/civis
        """
        account = get_account(username=user__username)
        account_civis = account.civis
        serializer = CiviSerializer(account_civis, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def followers(self, request, user__username=None):
        """
        Gets the followers of the selected account
        /accounts/{username}/followers
        """
        account = get_account(username=user__username)
        account_followers = account.followers.all()
        serializer = ProfileListSerializer(account_followers, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def following(self, request, user__username=None):
        """
        Gets the followings of the selected account
        /accounts/{username}/following
        """
        account = get_account(username=user__username)
        account_followings = account.following.all()
        serializer = ProfileListSerializer(account_followings, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def categories(self, request, user__username=None):
        """
        Gets the preferred categories of the selected account
        /accounts/{username}/categories
        """
        account = get_account(username=user__username)
        account_categories = account.categories
        serializer = CategorySerializer(account_categories, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def threads(self, request, user__username=None):
        """
        Gets the preferred categories of the selected account
        /accounts/{username}/categories
        """
        user = get_account(username=user__username).user
        draft_threads = Thread.objects.filter(author=user).exclude(is_draft=False)
        serializer = ThreadSerializer(
            draft_threads, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True)
    def drafts(self, request, user__username=None):
        """
        Gets the draft threads of the selected account
        /accounts/{username}/drafts
        """
        user = get_account(username=user__username).user
        draft_threads = Thread.objects.filter(author=user, is_draft=False)
        serializer = ThreadSerializer(
            draft_threads, many=True, context={"request": request}
        )
        return Response(serializer.data)


def get_user(request, username):
    """
    USAGE:
        This is used to get a user
    """

    User = get_user_model()

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)

        return JsonResponse(model_to_dict(profile))
    except Profile.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))


def get_profile(request, username):
    """
    USAGE:
       This is used to get a user profile
    """

    User = get_user_model()

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        result = Profile.objects.summarize(profile)

        result["issues"] = []
        voted_solutions = Activity.objects.filter(
            user=user.id, civi__c_type="solution", activity_type__contains="pos"
        )

        solution_threads = voted_solutions.values("thread__id").distinct()

        for thread_id in solution_threads:
            t = Thread.objects.get(id=thread_id)
            solutions = []
            solution_civis = voted_solutions.filter(thread=thread_id).values_list(
                "civi__id", flat=True
            )
            for civi_id in solution_civis:
                c = Civi.objects.get(id=civi_id)
                vote = voted_solutions.get(civi__id=civi_id).activity_type
                vote_types = {"vote_pos": "Agree", "vote_vpos": "Strongly Agree"}
                solution_item = {
                    "id": c.id,
                    "title": c.title,
                    "body": c.body,
                    "user_vote": vote_types.get(vote),
                }
                solutions.append(solution_item)

            my_issue_item = {
                "thread_id": t.id,
                "thread_title": t.title,
                "category": t.category.name,
                "solutions": solutions,
            }
            result["issues"].append(my_issue_item)

        if request.user.username != username:
            ra = Profile.objects.get(user=request.user)
            if username in ra.following.all():
                result["follow_state"] = True
            else:
                result["follow_state"] = False

        return JsonResponse(result)

    except Profile.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))


def get_card(request, username):
    """
    USAGE:
        This is used to get a card
    """

    User = get_user_model()

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        result = Profile.objects.card_summarize(
            profile, Profile.objects.get(user=request.user)
        )
        return JsonResponse(result)
    except User.DoesNotExist:
        return HttpResponseBadRequest(reason=f"User with username {username} not found")
    except Profile.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))


def get_feed(request):
    """
    USAGE:
       This is used to get a feed for a user
    """
    try:
        feed_threads = [
            Thread.objects.summarize(t) for t in Thread.objects.order_by("-created")
        ]

        return json_response(feed_threads)

    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))


@login_required
def edit_user(request):
    """
    Edit Profile Model
    """
    request_data = request.POST
    user = request.user
    account = Profile.objects.get(user=user)

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

    return JsonResponse(Profile.objects.summarize(account))


@login_required
def upload_profile_image(request):
    """ This function is used to allow users to upload profile photos """
    if request.method == "POST":
        form = UpdateProfileImage(request.POST, request.FILES)
        if form.is_valid():
            try:
                account = Profile.objects.get(user=request.user)

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

            except Profile.DoesNotExist:
                response = {"message": f"Profile with user {request.user.username} does not exist",
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
def clear_profile_image(request):
    """ This function is used to delete a profile image """
    if request.method == "POST":
        try:
            account = Profile.objects.get(user=request.user)

            # Clean up previous image
            account.profile_image.delete()
            account.save()

            return HttpResponse("Image Deleted")
        except Profile.DoesNotExist:
            return HttpResponseServerError(reason=f"Profile with id:{request.user.username} does not exist")
        except Exception:
            return HttpResponseServerError(reason=str("default"))
    else:
        return HttpResponseForbidden("allowed only via POST")


@login_required
@require_post_params(params=["target"])
def request_follow(request):
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

    User = get_user_model()

    try:
        account = Profile.objects.get(user=request.user)
        target = User.objects.get(username=request.POST.get("target", -1))
        target_account = Profile.objects.get(user=target)

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
    except Profile.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
@require_post_params(params=["target"])
def request_unfollow(request):
    """
    USAGE:
        Takes in user_id from current friend_requests list and joins accounts as friends.
        Does not join accounts as friends unless the POST friend is a valid member of the friend request array.

    Text POST:
        friend

    :return: (200, okay, list of friend information) (400, bad lookup) (500, error)
    """

    User = get_user_model()

    try:
        username = request.POST.get("target")
        if username:
            account = Profile.objects.get(user=request.user)
            target = User.objects.get(username=username)
            target_account = Profile.objects.get(user=target)

            account.following.remove(target_account)
            account.save()
            target_account.followers.remove(account)
            target_account.save()
            return JsonResponse({"result": "Success"})
        return HttpResponseBadRequest(reason="username cannot be empty")

    except User.DoesNotExist:
        return HttpResponseBadRequest(reason=f"User with username {username} does not exist")
    except Profile.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
def edit_user_categories(request):
    """
    USAGE:
        Edits list of categories for the user

    """
    try:
        account = Profile.objects.get(user=request.user)
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
    except Profile.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseServerError(reason=str(e))
