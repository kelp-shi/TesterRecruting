from django.urls import path
from baseApp.views.utillity import index
from baseApp.views.application.posts import *
from baseApp.views.application.utility import *
from baseApp.views.dm.dmControl import ThreadListView, MessageDetailView
from baseApp.views.auth.authControl import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from baseApp.sitemap import IndexSitemap, NewsSitemap, NewslistSitemap, ContactSitemap, RegisterSitemap

app_name = 'baseApp'

sitemaps = {
    'index':IndexSitemap,
    'news':NewsSitemap,
    'newslist':NewslistSitemap,
    'contact':ContactSitemap,
    'register':RegisterSitemap
}

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
    #申し込みページ
    path('detail/<int:pk>/join/', ApplyTask.as_view(), name='ApplyTask'),
    #申し込み者リスト
    path('detail/<int:pk>/applylist/', Authorization.as_view(), name='Authorization'),

    #----------DM----------
    #スレッドページ
    path('threads/', ThreadListView.as_view(), name='thread_list'),
    #DMページ
    path('threads/<int:room_id>/', MessageDetailView.as_view(), name='message_detail'),

    #----------other----------
    #ニュースリスト
    path('news/', newslist.as_view(), name='newslist'),
    #ニュース詳細
    path('news/<int:pk>', newsDetail.as_view(), name='newsDetail'),
    #コンタクトページ
    path('contact/', contact.as_view(), name='contact'),

    #----------account----------
    #登録画面
    path('register/', Register.as_view(), name='register'),
    #プロフィール画面
    path('profile/<str:username>/', Profile.as_view(), name='profile'),
    #プロフイール更新
    path('profile-edit/<str:username>/', ProfileEdit.as_view(), name='ProfileEdit'),
    #ログアウト
    path('logout/', LogoutView.as_view(), name='logout'),
    #仮登録画面
    path('register/done/', RegisterDone.as_view(), name='registerDone'),
    #本登録画面
    path('register/complete/<token>/', RegisterComplete.as_view(), name='registerComplete'),
    #----------account変更関連----------
    #パスワードリセット（ユーザー）
    path('reset/password/user/', ResetPasswordActive.as_view(), name='resetPasswordActive'),
    #パスワードリセット（未ログイン）
    path('reset/password/anonymouse/', ResetPasswordAnonymous.as_view(), name='resetPasswordAnonymouse'),
    #パスワードリセット完了
    path('reset/password/done/', PasswordResetDone.as_view(), name='passwordResetDone'),
    #パスワード変更（ユーザー）
    path('change/password/user/<token>/', ChangePasswordActive.as_view(), name='changePasswordActive'),
    #パスワード変更（未ログイン）
    path('change/password/anonymouse/<token>/', ChangePasswordAnonymous.as_view(), name='changePasswordAnonymous'),
    #パスワード変更完了（未ログイン）
    path('change/password/done/', ChangePasswordDone.as_view(), name='changePasswordDone'),
    #メールアドレスリセット
    path('reset/email/', ResetEmail.as_view(), name='resetEmail'),
    #メールアドレス変更
    path('change/email/<token>/', ChangeEmail.as_view(), name='changeEmail'),
    #ユーザーネーム請求
    path('usernameReq/', UsernameRequest.as_view(), name='usernameRequest'),

    #サイトマップ
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    #クロール用robots.txt
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'))
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)