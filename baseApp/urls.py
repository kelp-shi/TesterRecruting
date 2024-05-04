from django.urls import path
from . import views
from .views.header import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #----------app----------
    #index
    path('', index.as_view(), name='index'),
    #テスト一覧表示ページ（検索含む）
    path('postlist/', postlist.as_view(), name='postlist'),
    #テスト詳細ページ
    path('detail/', detail.as_view(), name='detail'),
    #ヘルプページ
    path('help/', help.as_view(), name='help'),
    #----------account----------
    #ウェルカムページ
    path('welcome/', welcome.as_view(), name='welcome'),
    #登録画面
    path('account/register/', register.as_view(), name='register'),
    #プロフィール画面
    path('account/profile/', profile.as_view(), name='profile'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),