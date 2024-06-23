from django.contrib import admin
from baseApp.db.application.app_models import *
from baseApp.models import CustomUser
from baseApp.db.application.dm_models import *
from baseApp.db.application.utillity_models import *


admin.site.register(TestPost)
admin.site.register(JoinRequest)
admin.site.register(CustomUser)
admin.site.register(DmRoom)
admin.site.register(Massage)

class BannerImages(admin.ModelAdmin):
    list_display = ('bannerTitle', 'bannerTitle', 'activeFlg')

admin.site.register(BannerImg)