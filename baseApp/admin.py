from django.contrib import admin
from .models.models import TestPost
from users.models import CustomUser

admin.site.register(TestPost)
admin.site.register(CustomUser)