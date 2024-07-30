import csv
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from baseApp.models import CustomUser
from baseApp.db.application.utillity_models import news
from baseApp.forms.application_forms import contactForm

class contact(LoginRequiredMixin, TemplateView):
    template_name = 'app/contact.html'

    def get(self, request, *args, **kwargs):
        form = contactForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = contactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # メール送信
            send_mail(
                f'お問い合わせ from {name}',
                message,
                email,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


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
