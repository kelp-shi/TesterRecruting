from django.contrib import admin
from .db.application.app_models import TestPost
from .models import CustomUser

admin.site.register(TestPost)
admin.site.register(CustomUser)