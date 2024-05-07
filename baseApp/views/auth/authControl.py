from django.views.generic import CreateView
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from ...forms.auth_forms import SignUpForm

class SignUpView(CreateView):
    form = SignUpForm
    template_name = ""
    success_url = reverse_lazy("baseApp:index")

    def form_invalid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())
