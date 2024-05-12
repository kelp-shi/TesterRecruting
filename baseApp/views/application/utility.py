from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class appHelp(LoginRequiredMixin,TemplateView):
    """
    ヘルプページ表示クラス

    Note:app/help.htmlのヘルプページを返す
    """
    template_name = 'app/help.html'