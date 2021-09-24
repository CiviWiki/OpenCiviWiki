import json
import datetime
import collections
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.forms.models import model_to_dict

from .models import Thread, Civi, Activity
from accounts.models import Profile


def json_custom_parser(obj):
    """
    A custom json parser to handle json.dumps calls properly for Decimal and Datetime data types.
    """
    if isinstance(obj, Decimal):
        return str(obj)
    elif not isinstance(obj, basestring) and isinstance(obj, collections.Iterable):
        return list(obj)
    elif isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        dot_ix = 19  # 'YYYY-MM-DDTHH:MM:SS.mmmmmm+HH:MM'.find('.')
        return obj.isoformat()[:dot_ix]
    else:
        raise TypeError(obj)


def json_response(data, status=200):
    return HttpResponse(
        json.dumps(data, default=json_custom_parser),
        content_type="application/json",
        status=status,
    )

def get_user(request, user):
    """
    USAGE:
        This is used to get a user
    """

    User = get_user_model()

    try:
        u = User.objects.get(username=user)
        a = Profile.objects.get(user=u)

        return JsonResponse(model_to_dict(a))
    except Profile.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))


def get_card(request, user):
    """
    USAGE:
        This is used to get a card
    """

    User = get_user_model()

    try:
        u = User.objects.get(username=user)
        a = Profile.objects.get(user=u)
        result = Profile.objects.card_summarize(
            a, Profile.objects.get(user=request.user)
        )
        return JsonResponse(result)
    except User.DoesNotExist:
        return HttpResponseBadRequest(reason=f"User with username {user} not found")
    except Profile.DoesNotExist as e:
        return HttpResponseBadRequest(reason=str(e))
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))


def get_profile(request, user):
    """
    USAGE:
       This is used to get a user profile
    """

    User = get_user_model()

    try:
        u = User.objects.get(username=user)
        a = Profile.objects.get(user=u)
        result = Profile.objects.summarize(a)

        result["issues"] = []
        voted_solutions = Activity.objects.filter(
            account=a.id, civi__c_type="solution", activity_type__contains="pos"
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

        if request.user.username != user:
            ra = Profile.objects.get(user=request.user)
            if user in ra.following.all():
                result["follow_state"] = True
            else:
                result["follow_state"] = False

        return JsonResponse(result)

    except Profile.DoesNotExist as e:
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


def get_thread(request, thread_id):
    """
    USAGE:
       This is used to get a requested thread
    """
    try:
        t = Thread.objects.get(id=thread_id)
        civis = Civi.objects.filter(thread_id=thread_id)
        req_a = Profile.objects.get(user=request.user)

        # TODO: move order by to frontend or accept optional arg
        c = civis.order_by("-created")
        c_scores = [ci.score(req_a.id) for ci in c]
        c_data = [Civi.objects.serialize_s(ci) for ci in c]

        problems = []
        for idx, item in enumerate(c_data):
            problems[idx]["score"] = c_scores[idx]

        data = {
            "title": t.title,
            "summary": t.summary,
            "tags": t.tags.all().values(),
            "author": {
                "username": t.author.user.username,
                "profile_image": t.author.profile_image.url
                if t.author.profile_image
                else "/media/profile/default.png",
                "first_name": t.author.first_name,
                "last_name": t.author.last_name,
            },
            "category": model_to_dict(t.category),
            "created": t.created,
            "contributors": [
                Profile.objects.chip_summarize(a)
                for a in Profile.objects.filter(
                    pk__in=civis.distinct("author").values_list("author", flat=True)
                )
            ],
            "num_civis": t.num_civis,
            "num_views": t.num_views,
            "votes": [
                {
                    "civi_id": act.civi.id,
                    "activity_type": act.activity_type,
                    "acct": act.account.id,
                }
                for act in Activity.objects.filter(thread=t.id, account=req_a.id)
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
        req_acct = Profile.objects.get(user=request.user)
        c_qs = Civi.objects.get(id=civi_id).responses.all()
        c_scored = []
        for res_civi in c_qs:
            c_dict = res_civi.dict_with_score(req_acct.id)
            c_rebuttal = res_civi.responses.all()
            if c_rebuttal:
                c_dict["rebuttal"] = c_rebuttal[0].dict_with_score(req_acct.id)
            c_scored.append(c_dict)

        civis = sorted(c_scored, key=lambda c: c["score"], reverse=True)

        return JsonResponse(civis, safe=False)
    except Profile.DoesNotExist:
        return HttpResponseBadRequest(reason=f"Profile with user:{request.user.username} does not exist")
    except Civi.DoesNotExist:
        return HttpResponseBadRequest(reason=f"Civi with id:{civi_id} does not exist")
    except Exception as e:
        return HttpResponseBadRequest(reason=str(e))
