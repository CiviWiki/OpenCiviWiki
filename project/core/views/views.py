from core.custom_decorators import full_profile, login_required
from django.template.response import TemplateResponse


@login_required
@full_profile
def create_group(request):
    return TemplateResponse(request, "newgroup.html", {})


def declaration(request):
    return TemplateResponse(request, "declaration.html", {})


def landing_view(request):
    return TemplateResponse(request, "landing.html", {})


def how_it_works_view(request):
    return TemplateResponse(request, "how_it_works.html", {})


def about_view(request):
    return TemplateResponse(request, "about.html", {})


def support_us_view(request):
    return TemplateResponse(request, "support_us.html", {})
