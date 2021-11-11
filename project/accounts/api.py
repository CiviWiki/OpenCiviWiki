from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseServerError,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from notifications.signals import notify

from accounts.permissions import IsProfileOwnerOrDuringRegistrationOrReadOnly
from accounts.serializers import (
    ProfileSerializer,
    ProfileListSerializer,
    UserSerializer,
)
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
    REST API ViewSet for an Profile
    retrieve:
    Return the given user based a username.

    list:
    Return a list of all the existing user profile. Only with privileged access.
    """

    queryset = Profile.objects.all()
    lookup_field = "user__username"
    serializer_class = ProfileSerializer
    http_method_names = ["get", "head", "put", "patch"]
    permission_classes = (IsProfileOwnerOrDuringRegistrationOrReadOnly,)

    def list(self, request):
        """ """
        if self.request.user.is_staff:
            profiles = Profile.objects.all()
        else:
            profiles = Profile.objects.filter(user=self.request.user)
        serializer = ProfileListSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, user__username=None):
        """ """
        profile = get_account(username=user__username)
        if self.request.user == profile.user:
            serializer = ProfileSerializer(profile)
        else:
            serializer = ProfileListSerializer(profile)
        return Response(serializer.data)

    @action(detail=True)
    def civis(self, request, user__username=None):
        """
        Gets the civis of the selected user account
        /accounts/{username}/civis
        """
        user = get_object_or_404(get_user_model(), username=user__username)
        user_civis = user.civis
        serializer = CiviSerializer(user_civis, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def followers(self, request, user__username=None):
        """
        Gets the followers of the selected user account
        /accounts/{username}/followers
        """
        profile = get_account(username=user__username)
        followers = profile.followers.all()
        serializer = ProfileListSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def following(self, request, user__username=None):
        """
        Gets the followings of the selected user account
        /accounts/{username}/following
        """
        profile = get_account(username=user__username)
        followings = profile.following.all()
        serializer = ProfileListSerializer(followings, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def categories(self, request, user__username=None):
        """
        Gets the preferred categories of the selected user account
        /accounts/{username}/categories
        """
        profile = get_account(username=user__username)
        categories = profile.categories
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def threads(self, request, user__username=None):
        """
        Gets the published threads of the selected user account
        /accounts/{username}/threads
        """
        user = get_user_model().objects.get(username=user__username)
        published_threads = Thread.objects.filter(author=user, is_draft=False)
        serializer = ThreadSerializer(
            published_threads, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True)
    def drafts(self, request, user__username=None):
        """
        Gets the draft threads of the selected account
        /accounts/{username}/drafts
        """
        user = get_user_model().objects.get(username=user__username)
        draft_threads = Thread.objects.filter(author=user, is_draft=True)
        serializer = ThreadSerializer(
            draft_threads, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ["list"]:
            self.permission_classes = [
                IsAuthenticated,
                IsProfileOwnerOrDuringRegistrationOrReadOnly,
            ]
        return super(ProfileViewSet, self).get_permissions()


@api_view(["GET"])
def get_user(request, username):
    """
    USAGE:
        This is used to get a user
    """

    try:
        user = get_user_model().objects.get(username=username)
        return JsonResponse(UserSerializer(user).data)
    except get_user_model().DoesNotExist:
        return JsonResponse(
            {"error": f"User with username {username} not found"}, status=400
        )


@api_view(["GET"])
def get_profile(request, username):
    """
    USAGE:
       This is used to get a user profile
    """

    try:
        user = get_user_model().objects.get(username=username)
        profile = user.profile
        result = Profile.objects.summarize(profile)
        result["issues"] = []
        voted_solutions = Activity.objects.filter(
            user=user.id, civi__c_type="solution", activity_type__contains="pos"
        )

        solution_threads = voted_solutions.values("thread__id").distinct()
        for thread_id in solution_threads:
            thread = Thread.objects.get(id=thread_id)
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
                "thread_id": thread.id,
                "thread_title": thread.title,
                "category": thread.category.name,
                "solutions": solutions,
            }
            result["issues"].append(my_issue_item)

        if request.user.username != username:
            requested_profile = Profile.objects.get(user=request.user)
            if username in requested_profile.following.all():
                result["follow_state"] = True
            else:
                result["follow_state"] = False

        return JsonResponse(result)

    except get_user_model().DoesNotExist:
        return JsonResponse(
            {"error": f"User with username {username} not found"}, status=400
        )


@api_view(["GET"])
def get_card(request, username):
    """
    USAGE:
        This is used to get a card
    """

    try:
        user = get_user_model().objects.get(username=username)
        profile = user.profile
        result = Profile.objects.card_summarize(
            profile, Profile.objects.get(user=request.user)
        )
        return JsonResponse(result)
    except get_user_model().DoesNotExist:
        return JsonResponse(
            {"error": f"User with username {username} not found"}, status=400
        )
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

    profile = Profile.objects.get(user=request.user)
    data = {
        "first_name": request.POST.get("first_name", profile.first_name),
        "last_name": request.POST.get("last_name", profile.last_name),
        "about_me": request.POST.get("about_me", profile.about_me),
    }

    profile.__dict__.update(data)
    try:
        profile.save()
    except Exception as e:
        return HttpResponseServerError(reason=str(e))

    profile.refresh_from_db()

    return JsonResponse(Profile.objects.summarize(profile))


@login_required
def upload_profile_image(request):
    """This function is used to allow users to upload profile photos"""

    if request.method == "POST":
        form = UpdateProfileImage(request.POST, request.FILES)
        if form.is_valid():
            try:
                profile = Profile.objects.get(user=request.user)

                # Clean up previous image
                profile.profile_image.delete()

                # Upload new image and set as profile picture
                profile.profile_image = form.clean_profile_image()
                try:
                    profile.save()
                except Exception as e:
                    response = {"message": str(e), "error": "MODEL_SAVE_ERROR"}
                    return JsonResponse(response, status=400)

                request.session["login_user_image"] = profile.profile_image_thumb_url

                response = {"profile_image": profile.profile_image_url}
                return JsonResponse(response, status=200)

            except get_user_model().DoesNotExist:
                response = {
                    "message": f"{request.user.username} does not have profile",
                    "error": "ACCOUNT_ERROR",
                }
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
    """This function is used to delete a profile image"""

    if request.method == "POST":
        try:
            account = Profile.objects.get(user=request.user)

            # Clean up previous image
            account.profile_image.delete()
            account.save()

            return HttpResponse("Image Deleted")
        except get_user_model().DoesNotExist:
            return HttpResponseServerError(
                reason=f"Profile with id:{request.user.username} does not exist"
            )
        except Exception:
            return HttpResponseServerError(reason=str("default"))
    else:
        return HttpResponseForbidden("allowed only via POST")


@login_required
@require_post_params(params=["target"])
def request_follow(request):
    """
    USAGE:
        Takes in user_id from current friend_requests list
        and joins accounts as friends.

        Does not join accounts as friends unless the POST friend
        is a valid member of the friend request array.

    Text POST:
        friend

    :return: (200, okay, list of friend information) (400, bad lookup) (500, error)
    """

    target_username = request.POST.get("target", -1)
    if request.user.username == target_username:
        response = {"error": "You cannot follow yourself, silly!"}
        return JsonResponse(response, status=400)

    try:
        account = Profile.objects.get(user=request.user)
        target = get_user_model().objects.get(username=target_username)
        target_account = Profile.objects.get(user=target)

        account.following.add(target_account)
        account.save()
        target_account.followers.add(account)
        target_account.save()
        data = {"username": target.username, "follow_status": True}

        notify.send(
            request.user,  # Actor User
            recipient=target,  # Target User
            verb="is following you",  # Verb
            target=target_account,  # Target Object
            popup_string="{user} is now following you".format(user=account.full_name),
            link="/{}/{}".format("profile", request.user.username),
        )

        return JsonResponse({"result": data})
    except get_user_model().DoesNotExist:
        return JsonResponse(
            {"error": f"User with username {target_username} not found"}, status=400
        )
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
@require_post_params(params=["target"])
def request_unfollow(request):
    """
    USAGE:
        Takes in user_id from current friend_requests list and
        joins accounts as friends.
        Does not join accounts as friends unless the POST
        friend is a valid member of the friend request array.

    Text POST:
        friend

    :return: (200, okay, list of friend information) (400, bad lookup) (500, error)
    """

    username = request.POST.get("target")
    try:
        if username:
            account = Profile.objects.get(user=request.user)
            target = get_user_model().objects.get(username=username)
            target_account = Profile.objects.get(user=target)

            account.following.remove(target_account)
            account.save()
            target_account.followers.remove(account)
            target_account.save()
            return JsonResponse({"result": "Success"})
        return JsonResponse({"error": "username cannot be empty"}, status=400)

    except get_user_model().DoesNotExist:
        return JsonResponse(
            {"error": f"User with username {username} not found"}, status=400
        )
    except Exception as e:
        return HttpResponseServerError(reason=str(e))


@login_required
def edit_user_categories(request):
    """
    USAGE:
        Edits list of categories for the user
    """
    try:
        profile = Profile.objects.get(user=request.user)
        categories = [int(i) for i in request.POST.getlist("categories[]")]
        profile.categories.clear()
        for category in categories:
            profile.categories.add(Category.objects.get(id=category))
            profile.save()

        data = {
            "user_categories": list(profile.categories.values_list("id", flat=True))
            or "all_categories"
        }
        return JsonResponse({"result": data})
    except get_user_model().DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseServerError(reason=str(e))
