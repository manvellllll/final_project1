from django.contrib import admin

# Register your models here.
from .models import Announcement, AppUser, UserLog


admin.site.register(Announcement)
admin.site.register(AppUser)
admin.site.register(UserLog)