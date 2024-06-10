from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,TemplateView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout
from django.core.signing import loads, BadSignature, SignatureExpired, dumps
from baseApp.forms.auth_forms import SignUpForm, SignInForm, ProfileEditForm
from django.template.loader import render_to_string
from baseApp.models import CustomUser
from testerRecruting.settings import ACTIVATION_TIMEOUT_SECONDS
from django.http import Http404, HttpResponseBadRequest
import logging
from baseApp.views.auth.utility import imageConvert, imageNameSelect, errorEmailSender
from datetime import date

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
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        editform = ProfileEditForm(instance=user)
        return render(request, self.template_name, {'editform': editform, 'user': user})
    
    def post(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        editform = ProfileEditForm(request.POST, request.FILES, instance=user)
        #プロフイール編集フォーム バリデーションチェック
        if editform.is_valid():
            user_birth = editform.cleaned_data['UserBirth']
            today = date.today()
            # 年齢計算
            age = today.year - user_birth.year - ((today.month, today.day) < (user_birth.month, user_birth.day))
            user.UserBirth = user_birth
            user.UserGender = editform.cleaned_data['UserGender']
            #プロフィール画像アップロード有無確認
            if request.FILES.get('profile_img'):
                beforeImg = request.FILES['profile_img']
                #画像をjpgに変換
                afterImg = imageConvert(beforeImg)
                #画像名称をランダム設定
                imgName = imageNameSelect()
                user.profile_img.save(imgName, afterImg)
            user.age = age  # Save the calculated age
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



