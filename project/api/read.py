from django.http import JsonResponse, HttpResponseBadRequest
from django.forms.models import model_to_dict

from .models import Thread, Civi, Activity
from accounts.models import Profile
from .utils import json_response


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
