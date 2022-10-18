from accounts.models import Profile
from core.custom_decorators import require_post_params
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError, JsonResponse
from notifications.signals import notify


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
