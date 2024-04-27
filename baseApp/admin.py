from django.contrib import admin
from .models.application.model import TestPost
from testerRecruting.baseApp.models.users.models import CustomUser

admin.site.register(TestPost)
admin.site.register(CustomUser)