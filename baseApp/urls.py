from django.urls import path
from .views.header import index
from .views.application.posts import createTask, TestPostSearchView, PostDetail
from .views.application.utility import appHelp
from django.conf import settings
from django.conf.urls.static import static

app_name = 'baseApp'

urlpatterns = [
    #----------app----------
    #index
    path('', index.as_view(), name='index'),
    #テスト投稿ページ
    path('createpost/', createTask.as_view(), name='createpost'),
    #テスト一覧表示ページ（検索含む）
    path('postlist/', TestPostSearchView.as_view(), name='postlist'),
    #テスト詳細ページ
    path('detail/<int:pk>/', PostDetail.as_view(), name='detail'),
    #ヘルプページ
    path('help/', appHelp.as_view(), name='help'),
    #----------account----------
    #ウェルカムページ
    #path('welcome/', welcome.as_view(), name='welcome'),
    #登録画面
    #path('account/register/', register.as_view(), name='register'),
    #プロフィール画面
    #path('account/profile/', profile.as_view(), name='profile'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)