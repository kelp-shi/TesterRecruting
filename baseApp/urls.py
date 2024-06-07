from django.urls import path
from .views.header import index
from .views.application.posts import createTask, TestPostSearchView, PostDetail
from .views.application.utility import appHelp
from .views.auth.authControl import Profile, Register, LogoutView, RegisterDone, RegisterComplete
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
    #登録画面
    path('register/', Register.as_view(), name='register'),
    #プロフィール画面
    path('profile/<str:username>/', Profile.as_view(), name='profile'),
    #ログアウト
    path('logout/', LogoutView.as_view(), name='logout'),
    #仮登録画面
    path('register/done/', RegisterDone.as_view(), name='registerDone'),
    #本登録画面
    path('register/complete/', RegisterComplete.as_view(), name='registerComplete')
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)