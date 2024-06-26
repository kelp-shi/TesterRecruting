from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from baseApp.db.application.app_models import TestPost
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
        context['user'] = self.request.user
        context['newposts'] = TestPost.objects.filter(RecrutingPeriodFlg=True).order_by('RecrutingPeriodSt')[:3]
        context['recomendpost'] = TestPost.objects.filter(RecrutingPeriodFlg=True).order_by('?')[:10]
        return context