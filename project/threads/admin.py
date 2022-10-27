from django.contrib import admin

from .models import (
    Activity,
    Civi,
    CiviImage,
    Fact,
    Rationale,
    Rebuttal,
    Response,
    Thread,
)

admin.site.register(Fact)
admin.site.register(Thread)
admin.site.register(Civi)
admin.site.register(Response)
admin.site.register(CiviImage)
admin.site.register(Activity)
admin.site.register(Rebuttal)
admin.site.register(Rationale)
