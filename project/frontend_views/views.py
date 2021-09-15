import json

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse


from api.models import Category, Thread, Civi, Activity
from accounts.models import Profile
from accounts.forms import UpdateProfile
from api.forms import UpdateProfileImage
from core.constants import US_STATES
from core.custom_decorators import login_required, full_account

from django.contrib.auth import get_user_model

User = get_user_model()


def base_view(request):
    if not request.user.is_authenticated:
        return TemplateResponse(request, "static_templates/landing.html", {})

    a = Profile.objects.get(user=request.user)
    if "login_user_image" not in request.session.keys():
        request.session["login_user_image"] = a.profile_image_thumb_url

    categories = [{"id": c.id, "name": c.name} for c in Category.objects.all()]

    all_categories = list(Category.objects.values_list("id", flat=True))
    user_categories = list(a.categories.values_list("id", flat=True)) or all_categories

    feed_threads = [
        Thread.objects.summarize(t)
        for t in Thread.objects.exclude(is_draft=True).order_by("-created")
    ]
    top5_threads = list(
        Thread.objects.filter(is_draft=False)
        .order_by("-num_views")[:5]
        .values("id", "title")
    )
    my_draft_threads = [
        Thread.objects.summarize(t)
        for t in Thread.objects.filter(author_id=a.id)
        .exclude(is_draft=False)
        .order_by("-created")
    ]

    states = sorted(US_STATES, key=lambda s: s[1])
    data = {
        "categories": categories,
        "states": states,
        "user_categories": user_categories,
        "threads": feed_threads,
        "trending": top5_threads,
        "draft_threads": my_draft_threads,
    }

    return TemplateResponse(request, "feed.html", {"data": json.dumps(data)})


@login_required
@full_account
def user_profile(request, username=None):
    if request.method == "GET":
        if not username:
            return HttpResponseRedirect("/profile/{0}".format(request.user))
        else:
            is_owner = username == request.user.username
            try:
                user = User.objects.get(username=username)
                account = user.account_set.first()
            except User.DoesNotExist:
                return HttpResponseRedirect("/404")

        form = UpdateProfile(
            initial={
                "username": user.username,
                "email": user.email,
                "first_name": account.first_name or None,
                "last_name": account.last_name or None,
                "about_me": account.about_me or None,
            },
            readonly=True,
        )
        data = {
            "username": user,
            "profile_image_form": UpdateProfileImage,
            "form": form if is_owner else None,
            "readonly": True,
        }
        return TemplateResponse(request, "account.html", data)


@login_required
def user_setup(request):
    a = Profile.objects.get(user=request.user)
    if a.full_account:
        return HttpResponseRedirect("/")
        # start temp rep rendering TODO: REMOVE THIS
    else:
        data = {
            "username": request.user.username,
            "email": request.user.email,
        }
        return TemplateResponse(request, "user-setup.html", data)


@login_required
@full_account
def issue_thread(request, thread_id=None):
    if not thread_id:
        return HttpResponseRedirect("/404")

    req_acct = Profile.objects.get(user=request.user)
    t = Thread.objects.get(id=thread_id)
    c_qs = Civi.objects.filter(thread_id=thread_id).exclude(c_type="response")
    c_scored = [c.dict_with_score(req_acct.id) for c in c_qs]
    civis = sorted(c_scored, key=lambda c: c["score"], reverse=True)

    # modify thread view count
    t.num_civis = len(civis)
    t.num_views = F("num_views") + 1
    t.save()
    t.refresh_from_db()

    thread_wiki_data = {
        "thread_id": thread_id,
        "title": t.title,
        "summary": t.summary,
        "image": t.image_url,
        "author": {
            "username": t.author.user.username,
            "profile_image": t.author.profile_image_url,
            "first_name": t.author.first_name,
            "last_name": t.author.last_name,
        },
        "contributors": [
            Profile.objects.chip_summarize(a)
            for a in Profile.objects.filter(
                pk__in=civis.distinct("author").values_list("author", flat=True)
            )
        ],
        "category": {"id": t.category.id, "name": t.category.name},
        "categories": [{"id": c.id, "name": c.name} for c in Category.objects.all()],
        "states": sorted(US_STATES, key=lambda s: s[1]),
        "created": t.created_date_str,
        "level": t.level,
        "state": t.state if t.level == "state" else "",
        "location": t.level if not t.state else dict(US_STATES).get(t.state),
        "num_civis": t.num_civis,
        "num_views": t.num_views,
        "user_votes": [
            {
                "civi_id": act.civi.id,
                "activity_type": act.activity_type,
                "c_type": act.civi.c_type,
            }
            for act in Activity.objects.filter(thread=t.id, account=req_acct.id)
        ],
    }
    thread_body_data = {
        "civis": civis,
    }

    data = {
        "thread_id": thread_id,
        "is_draft": t.is_draft,
        "thread_wiki_data": json.dumps(thread_wiki_data),
        "thread_body_data": json.dumps(thread_body_data),
    }
    return TemplateResponse(request, "thread.html", data)


@login_required
@full_account
def create_group(request):
    return TemplateResponse(request, "newgroup.html", {})


def declaration(request):
    return TemplateResponse(request, "declaration.html", {})


def landing_view(request):
    return TemplateResponse(request, "static_templates/landing.html", {})


def how_it_works_view(request):
    return TemplateResponse(request, "static_templates/how_it_works.html", {})


def about_view(request):
    return TemplateResponse(request, "static_templates/about.html", {})


def support_us_view(request):
    return TemplateResponse(request, "static_templates/support_us.html", {})


""" CSV export function. Thread ID goes in, CSV HTTP response attachment goes out. """


@csrf_exempt
def civi2csv(request, thread_id):
    import csv

    thread = thread_id
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=" + thread + ".csv"
    writer = csv.writer(response, delimiter=",")
    for card in Civi.objects.filter(thread_id=thread):
        data = []
        for key, value in card.dict_with_score().items():
            if value:
                data.append(value)
        writer.writerow(data)
    return response
