import csv
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from baseApp.models import CustomUser

class appHelp(LoginRequiredMixin,TemplateView):
    """
    ヘルプページ表示クラス

    Note:app/help.htmlのヘルプページを返す
    """
    template_name = 'app/help.html'

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