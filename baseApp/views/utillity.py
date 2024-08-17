from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from baseApp.db.application.app_models import TestPost
from baseApp.db.application.dm_models import DmRoom, Massage
from baseApp.db.application.utillity_models import BannerImg
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils import timezone
from baseApp.models import CustomUser
import random, string
import logging

logger = logging.getLogger(__name__)

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

def combine_date(year, month, day):
    current_time = timezone.now()
    year = int(year)
    month = int(month)
    day = int(day)
    date_str = f"{year:04d}-{month:02d}-{day:02d} {current_time.strftime('%H:%M:%S,%f')}"
    return timezone.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S,%f")

def errorEmailSender(self, errorMsg):
    """
    管理者へエラーメッセージを送付する
    """
    user = CustomUser.objects.get(self)
    current_site = get_current_site(self.request)
    domain = current_site.domain
    context = {
        'protocol': self.request.scheme,
        'domain': domain,
        'errorMsg': errorMsg,
    }
    # サブジェクト
    subject = render_to_string('admin/email/subject.txt', context)
    # メッセージ
    message = render_to_string('admin/email/message.txt', context)
    user.email_user(subject, message)

class index(LoginRequiredMixin, TemplateView):
    """
    indexビュー
    """

    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        # 自身の情報
        current_user = self.request.user
        context = super().get_context_data(**kwargs)
        # ログインユーザ情報
        context['user'] = current_user
        # 新規ポスト(3件)
        context['newposts'] = TestPost.objects.filter(RecrutingPeriodFlg=True, DelFlg=False).order_by('RecrutingPeriodSt')[:3]
        # おすすめポスト(10件)
        context['recomendpost'] = TestPost.objects.filter(RecrutingPeriodFlg=True, DelFlg=False).order_by('?')[:10]
        # 自身のDM
        my_dms = DmRoom.objects.filter(Member=current_user)
        # バナー画像を取得
        banner_info = BannerImg.objects.filter(activeFlg=True)
        

        other_members = {}
        new_message = {}
        for room in my_dms:
            other_member = room.Member.exclude(id=current_user.id).first()  # 他のメンバーを取得
            my_message = Massage.objects.filter(Room=room.id).latest('Created_at')
            print(my_message)
            if other_member:
                other_members[room.id] = other_member
                new_message[room.id] = my_message
                print(new_message)

        context['rooms'] = my_dms
        context['other_members'] = other_members
        context['dmMessage'] = new_message
        context['banner'] = banner_info

        return context