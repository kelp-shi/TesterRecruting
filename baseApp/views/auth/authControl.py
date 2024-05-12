from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView,TemplateView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from ...forms.auth_forms import SignUpForm
from ...models import CustomUser

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

class Register(CreateView):
    """
    登録・ログインページ

    Note:auth/register.htmlのヘルプページを返す
    """
    template_name = 'auth/register.html'
    success_url = reverse_lazy("baseApp:index")

    def login(request):
        if request.method == 'POST':
            form = SignUpForm
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                UserBirth = form.cleaned_data.get('UserBirth')
                UserGender = form.cleaned_data.get('UserGender')
                profile_img = form.cleaned_data.get('profile_img')
                age = form.cleaned_data.get('age')

    



