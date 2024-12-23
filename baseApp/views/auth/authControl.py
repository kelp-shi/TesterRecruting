from django.views import View
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout
from django.views.generic import DetailView,TemplateView
from django.template.loader import render_to_string
from django.core.signing import loads, BadSignature, SignatureExpired, dumps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site

from testerRecruting.settings import ACTIVATION_TIMEOUT_SECONDS
from baseApp.forms.auth_forms import SignUpForm, SignInForm, ProfileEditForm
from baseApp.models import CustomUser
from baseApp.views.auth.utility import imageConvert, imageNameSelect
from baseApp.views.utillity import errorEmailSender

from datetime import date
import logging

logger = logging.getLogger(__name__)
errorMail = errorEmailSender
    
class Profile(LoginRequiredMixin,DetailView):
    """
    プロフィールページ

    note:プロフィールページ出力クラス
    auth/profile.htmlのページを返す
    """
    template_name = "auth/profile.html"
    model = CustomUser
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = CustomUser.objects.all()
    context_object_name = 'profile'

class ProfileEdit(LoginRequiredMixin, View):
    """
    プロフイール編集ページ
    """
    template_name = 'auth/profileEdit.html'
    
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        editform = ProfileEditForm(instance=user)
        return render(request, self.template_name, {'editform': editform, 'user': user})
    
    def post(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        editform = ProfileEditForm(request.POST, request.FILES, instance=user)
        #プロフイール編集フォーム バリデーションチェック
        if editform.is_valid():
            user_birth = editform.cleaned_data.get('UserBirth')
            user_gender = editform.cleaned_data.get('UserGender')
            email_for_test = editform.cleaned_data.get('email_for_test')
            bio = editform.cleaned_data.get('bio_text')
            profile_img = request.FILES.get('profile_img')

            if user_birth:
                today = date.today()
                age = today.year - user_birth.year - ((today.month, today.day) < (user_birth.month, user_birth.day))
                user.UserBirth = user_birth
                user.age = age

            if email_for_test:
                user.email_for_test = email_for_test
            
            if user_gender:
                user.UserGender = user_gender

            if bio:
                user.bio_text = bio

            if profile_img:
                beforeImg = profile_img
                afterImg = imageConvert(beforeImg)
                imgName = imageNameSelect()
                user.profile_img.save(imgName, afterImg)
            elif not user.profile_img: user.profile_img = None # 既存の画像がない場合にNoneを設定
            
            user.save()
            return redirect('baseApp:profile', username=username)

        return render(request, self.template_name, {'editform': editform, 'user': user})
            

class LogoutView(View):
    """
    ログアウトページ

    Note:リダイレクト先（登録・ログインページ）
    """
    def get(self, request):
        logout(request)
        return redirect('baseApp:register')

class Register(TemplateView):
    """
    登録・ログインページ

    Note:auth/register.htmlのヘルプページを返す
    """
    template_name = 'auth/register.html'

    logger.debug('------------method start------------')
    def post(self, request, *args, **kwargs):
        form_up = SignUpForm(data=request.POST)
        form_in = SignInForm(data=request.POST)
        if 'logon_btn' in request.POST:
            # ユーザー登録バリデーションチェック
            # Trueであった場合、仮登録し認証メールを飛ばす
            if form_up.is_valid():
                username = form_up.cleaned_data.get('username')
                if username == 'username':
                    logger.error(form_up.errors.as_json())
                    return render(request, 'auth/register.html', {'form_up': form_up, 'form_in': form_in, 'error_user':'Please use a name other than username'})
                user = form_up.save(commit=False)
                user.is_active = False
                user.save()
                # アクティベーションURLの送付
                current_site = get_current_site(self.request)
                domain = current_site.domain
                context = {
                    'protocol': self.request.scheme,
                    'domain': domain,
                    'token': dumps(user.pk),
                    'user': user,
                }
                # サブジェクト
                subject = render_to_string('auth/mail/subject.txt', context)
                # メッセージ
                message = render_to_string('auth/mail/message.txt', context)

                user.email_user(subject, message)
                return redirect('baseApp:registerDone')
            else:
                logger.error('------------logon error------------')
                logger.error(form_up.errors.as_json())
            return render(request, 'auth/register.html', {'form_up': form_up, 'form_in': form_in})
        
        elif 'login_btn' in request.POST :
            if form_in.is_valid():
                username = form_in.cleaned_data.get('username')
                user = CustomUser.objects.get(username=username)
                if user:
                    login(request, user)
                    return redirect("baseApp:index")
                else:
                    logger.debug('------------login error------------')
            logger.debug('------------method end------------')
            return render(request, 'auth/register.html', {'form_up': form_up, 'form_in': form_in})
        
        else:
            logger.error('auth_control method error')
            pass
            
    def get(self, request):
        logger.debug('------------get method start------------')
        form_up = SignUpForm()
        form_in = SignInForm()
        return render(request, 'auth/register.html', {'form_up': form_up, 'form_in': form_in})
    
class RegisterDone(TemplateView):
    """
    仮登録完了ページ
    """
    template_name = 'auth/registerDone.html'

class RegisterComplete(TemplateView):
    """
    本登録完了ページ

    Note:indexへリダイレクト
    """
    template_name = 'auth/registerComp.html'
    timeout_seconds = ACTIVATION_TIMEOUT_SECONDS

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()
        
        else:
            try:
                user = CustomUser.objects.get(pk=user_pk)
            except CustomUser.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)
        
        return HttpResponseBadRequest



