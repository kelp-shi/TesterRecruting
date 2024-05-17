from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView,TemplateView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from ...forms.auth_forms import SignUpForm, SignInForm
from ...models import CustomUser
import logging

logger = logging.getLogger(__name__)

class SignUpView(LoginRequiredMixin,CreateView):
    form = SignUpForm
    template_name = ""
    success_url = reverse_lazy("baseApp:index")

    def form_invalid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())
    
class Profile(LoginRequiredMixin,DetailView):
    template_name = "auth/profile.html"
    model = CustomUser
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = CustomUser.objects.all()
    context_object_name = 'profile'

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
                user = form_up.save()
                login(request, user)
                return redirect("baseApp:index")
            else:
                logger.debug('------------logon error------------')
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
            return render(request, 'auth/register.html', {'form_up': form_up, 'form_in': form_in})
        
        else:
            logger.debug('auth_control method error')
            pass
            
    def get(self, request, *args, **kwargs):
        form_up = SignUpForm()
        form_in = SignInForm()
        return render(request, 'auth/register.html', {'form_up': form_up, 'form_in': form_in}) 
