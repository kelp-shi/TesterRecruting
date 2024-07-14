import csv
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from baseApp.models import CustomUser
from baseApp.db.application.utillity_models import news

class contact(LoginRequiredMixin,TemplateView):
    """
    コンタクトページ表示クラス

    Note:app/help.htmlのヘルプページを返す
    """
    template_name = 'app/help.html'

class newslist(LoginRequiredMixin, ListView):
    """
    ニュースリスト表示クラス
    """
    template_name = 'app/newsList.html'
    model = news
    ordering = '-Create_at'

class exportEmailCsv():
    """
    メーリングリストをCSV出力する ※未実装
    """
    def get(self, request):
        # CSVのHTTPレスポンスを作成
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="emails.csv"'

        # CSVライターを作成
        writer = csv.writer(response)

        # ユーザーのメールアドレスを取得してCSVに書き込む
        users = CustomUser.objects.values_list('email', flat=True)
        for email in users:
            writer.writerow([email])

        return response
