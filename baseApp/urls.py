from django.urls import path
from . import views
from .views.defalt import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index.as_view(), name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)