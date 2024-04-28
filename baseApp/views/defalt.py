from typing import Any
from django import views
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import ListView,TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin
from ..db.application.app_models import TestPost
from ..models import CustomUser
import datetime


class index(LoginRequiredMixin, TemplateView):
    #model = TestPost
    #model = CustomUser
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context