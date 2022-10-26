from categories.models import Category
from django.contrib import admin
from notification.models import Notification
from threads.models import (
    Activity,
    Civi,
    CiviImage,
    Fact,
    Rationale,
    Rebuttal,
    Response,
    Thread,
)

from .models import Profile, User

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Fact)
admin.site.register(Thread)
admin.site.register(Civi)
admin.site.register(Response)
admin.site.register(CiviImage)
admin.site.register(Activity)
admin.site.register(Rebuttal)
admin.site.register(Rationale)
