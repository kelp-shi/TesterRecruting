from django.views import View
from django.shortcuts import redirect, render
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

logger = logging.getLogger(__name__)
    
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
    def get(self, request):
        editform = ProfileEditForm
        return render(request,  '', {'editform':editform})
    
    def post(self, request):
        editform = ProfileEditForm(request.POST or None)
        if editform.is_valid():
            user_date = CustomUser.objects.get(id=request.user.id)
            user_date.UserBirth = editform.cleaned_data['userBirth']
            user_date.UserGender = editform.cleaned_data['UserGender']
            if request.FILES.get('profile_img'):
                user_date.profile_img = editform.cleaned_data['profile_img']
            user_date.save()
            return redirect('baseApp:profile')
        return render(request, 'auth/profile.html')
            

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
    #success_url = reverse_lazy("baseApp:index")
    logger.debug('------------method start------------')
    def post(self, request, *args, **kwargs):
        form_up = SignUpForm(data=request.POST)
        form_in = SignInForm(data=request.POST)
        if 'logon_btn' in request.POST:
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

                subject = render_to_string('auth/mail/subject.txt', context) #テキストのURL
                message = render_to_string('auth/mail/message.txt', context) #テキストのURL

                user.email_user(subject, message)
                return redirect('baseApp:registerDone')
            else:
                logger.debug('------------logon error------------')
                logger.debug(form_up.errors.as_json())
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
            logger.debug('auth_control method error')
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



