from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from baseApp.db.application.app_models import TestPost
from baseApp.db.application.dm_models import DmRoom
from baseApp.models import CustomUser
import random, string

def randomString():
    """
    ランダムな文字列を作成
    """
    randomText = random.choice(string.ascii_letters + string.digits)
    return randomText

def randomNumver(length):
    """
    ランダムな数列を作成
    """
    digits = ''.join(random.choices(string.digits, k=length))
    return digits

class index(LoginRequiredMixin, TemplateView):
    """
    indexビュー
    """

    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログインユーザ情報
        context['user'] = self.request.user
        # 新規ポスト(３件)
        context['newposts'] = TestPost.objects.filter(RecrutingPeriodFlg=True).order_by('RecrutingPeriodSt')[:3]
        # おすすめポスト(10件)
        context['recomendpost'] = TestPost.objects.filter(RecrutingPeriodFlg=True).order_by('?')[:10]
        # 自身のDM
        my_dms = DmRoom.objects.filter(Member=self.request.user)
        context['mydms'] = my_dms
        # 自身のDMに関するメンバー情報の取得
        other_members = {}
        for dm in my_dms:
            other_users = dm.Member.exclude(id=self.request.user.id).values('username', 'profile_img')
            other_members[dm.id] = list(other_users)
        context['other_menbers'] = other_members
        return context