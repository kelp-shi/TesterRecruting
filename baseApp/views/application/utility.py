import csv
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from baseApp.models import CustomUser
from baseApp.db.application.utillity_models import news, BannerImg
from baseApp.forms.application_forms import contactForm
import logging
logger = logging.getLogger(__name__)

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
            try:
                send_mail(
                    f'お問い合わせ from {name} : {email}',
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    settings.CONTACT_EMAIL,
                    fail_silently=False,
                )
                return JsonResponse({'status': 'success'}, status=200)
            except Exception as e:
                print(f"Error sending email: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


class newslist(LoginRequiredMixin, ListView):
    """
    ニュースリスト表示クラス
    """
    template_name = 'app/newsList.html'
    model = news
    ordering = '-Create_at'

class newsDetail(LoginRequiredMixin, TemplateView):
    """
    newsのdetailを表示する
    """

    template_name = 'app/newsDetail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        newsdata = get_object_or_404(news, pk=self.kwargs['pk'])

        context['news'] = newsdata
        return context

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
