from django.views.generic import TemplateView

class appHelp(TemplateView):
    """
    ヘルプページ表示クラス

    Note:app/help.htmlのヘルプページを返す
    """
    template_name = 'app/help.html'