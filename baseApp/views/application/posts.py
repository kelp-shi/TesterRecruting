from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy
from ...db.application.app_models import TestPost
from django.contrib.auth.mixins import LoginRequiredMixin
from ...forms.application_forms import TestPostForm, ApplyForm
from baseApp.views.utillity import randomNumver
from django.shortcuts import get_object_or_404

import datetime
import logging

# Create your views here.
logger = logging.getLogger(__name__)

class createTask(LoginRequiredMixin, CreateView):
    """
    新規テストポストの作成
    """
    #model = TestPost
    form_class = TestPostForm
    template_name = 'app/createpost.html'

    def get_success_url(self):
        return reverse_lazy('baseApp:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # 投稿者を現在のユーザーに設定
        form.instance.id = randomNumver(10)
        form.instance.CreateUser = self.request.user
        response = super().form_valid(form)
        self.request.user.MyTest.add(form.instance)
        return response

    def form_invalid(self, form):
        logger.debug('---------------form is fail---------------')
        logger.debug(form.errors.as_json())
        return super().form_invalid(form)
    

class TestPostSearchView(LoginRequiredMixin,ListView):
    """
    テストポストの表示・検索
    Note:
    部分一致可:大小区別なし
    募集期日検索（期日が近い）
    募集期日検索（期日が遠い）
    テスト期日検索（期日が近い）
    テスト期日検索（期日が遠い）
    """
    logger.info('---------------start list method[TestPostSearchView]---------------')
    model = TestPost
    logger.info('model count: ' + str(model.objects.count()))
    logger.info('active model count: ' + str(model.objects.filter(RecrutingPeriodFlg=True, DelFlg=False).count()))
    template_name = 'app/postlist.html'
    # ページネーション
    paginate_by = 10

    @method_decorator(cache_page(60))  # キャッシュを60秒間有効にする
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        query = self.request.GET.get('query')
        sort_by = self.request.GET.get('sort_by')
        logger.debug('query type | sort: ' + str(sort_by) + ' | query: ' + str(query))
        logger.debug('---------------start get queryset[get_queryset]---------------')

        if query:
            # 名称検索（部分一致可:大小区別なし）
            queryset = TestPost.objects.filter(PostName__icontains=query)
        else:
            # テストポストの全件取得（条件：募集フラグ==True, 削除フラグ==Falese）
            queryset = TestPost.objects.filter(RecrutingPeriodFlg=True, DelFlg=False).order_by('id')

        logger.debug('end method -- ' + str(queryset.count()))
        return queryset
        
    def post(self):
        logger.debug('---------------start get queryset[post]---------------')
        now = datetime.datetime.now()
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            # データをソート
            if sort_by == 'recruting_up':
                # 募集期日検索（期日が近い）
                queryset = sorted(TestPost.objects.filter(RecrutingPeriodFlg=True, DelFlg=False), key=lambda post: abs(now - post.RecrutingPeriodSt))
            elif sort_by == 'recruting_down':
                # 募集期日検索（期日が遠い）
                queryset = sorted(TestPost.objects.filter(RecrutingPeriodFlg=True, DelFlg=False), key=lambda post: abs(now + post.RecrutingPeriodSt))
            elif sort_by == 'test_up':
                # テスト期日検索（期日が近い）
                queryset = sorted(TestPost.objects.filter(RecrutingPeriodFlg=True, DelFlg=False), key=lambda post: abs(now - post.TestStart))
            elif sort_by == 'test_down':
                # テスト期日検索（期日が遠い）
                queryset = sorted(TestPost.objects.filter(RecrutingPeriodFlg=True, DelFlg=False), key=lambda post: abs(now + post.TestStart))
            else:
                # 何も返さない場合は空のクエリセットを返す
                queryset = TestPost.objects.none()      

        logger.debug('end method -- ' + str(queryset.count()))
        logger.debug('---------------end get queryset---------------')
        return queryset
        
    def get_context_data(self, **kwargs):
        """
        検索結果が空の場合
        """
        logger.info('---------------start list method(non object)---------------')
        logger.debug('---------------start get queryset(non object)---------------')

        context = super().get_context_data(**kwargs)
        if not self.object_list.exists():
            context['no_results_message'] = '検索結果がありません。'

        logger.debug('---------------end get queryset(non object)---------------')
        logger.info('---------------end list method-(non object)[TestPostSearchView]--------------')
        return context

class PostDetail(LoginRequiredMixin,DetailView):
    """
    詳細クラス
    
    Note:テストポストの詳細を表示
    """
    model = TestPost
    template_name = 'app/detail.html'

    def get_context_data(self, **kwargs):
        logger.debug('---------------start get_context_method---------------')
        context = super().get_context_data(**kwargs)
        context['postdetail'] = TestPost.objects.all()
        logger.debug('set context')
        logger.debug('---------------end get_context_method---------------')
        return context
    
class ApplyTask(FormView):
    """
    申請クラス

    Note:詳細ページで応募ボタン押下時に呼び出される
    """
    form_class = ApplyForm
    template_name = ''

    def form_valid(self, form):
        post_id = self.kwargs['id']
        post = get_object_or_404(TestPost, id=post_id)
        return super().form_valid(form)
    
class authorization():
    """
    テストユーザー認可クラス ※未実装

    Note:申請を送ったユーザーを認証する
    """
    pass