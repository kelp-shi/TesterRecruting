from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import CustomUser


class index(LoginRequiredMixin, TemplateView):
    """
    indexビュー
    """
    model = CustomUser
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context