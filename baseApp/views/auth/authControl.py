from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from ...forms.auth_forms import SignUpForm
from ...models import CustomUser

class SignUpView(CreateView):
    form = SignUpForm
    template_name = ""
    success_url = reverse_lazy("baseApp:index")

    def form_invalid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())
    
class Profile(DetailView):
    template_name = "auth/profile.html"
    model = CustomUser
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = CustomUser.objects.all()
    context_object_name = 'profile'

