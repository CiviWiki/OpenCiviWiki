from django.template.response import TemplateResponse




def landing_view(request):
    return TemplateResponse(request, "static_templates/landing.html", {})


def how_it_works_view(request):
    return TemplateResponse(request, "static_templates/how_it_works.html", {})


def about_view(request):
    return TemplateResponse(request, "static_templates/about.html", {})


def support_us_view(request):
    return TemplateResponse(request, "static_templates/support_us.html", {})
