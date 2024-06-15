from django.contrib import admin
from baseApp.db.application.app_models import TestPost
from baseApp.models import CustomUser
from baseApp.db.application.dm_models import DmRoom, Massage


admin.site.register(TestPost)
admin.site.register(CustomUser)
admin.site.register(DmRoom)
admin.site.register(Massage)