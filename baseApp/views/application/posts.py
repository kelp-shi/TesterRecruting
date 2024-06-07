from django.views.generic import ListView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from ...db.application.app_models import TestPost
from django.contrib.auth.mixins import LoginRequiredMixin
from ...forms.application_forms import TestPostForm3
import datetime
import logging

# Create your views here.
logger = logging.getLogger(__name__)

class createTask(LoginRequiredMixin,CreateView):
    """
    新規テストポストの作成
    """
    model = TestPost
    template_name = 'app/createpost.html'
    fields = ['PostName']
    
    def post(request):
        # テストポストのフォーム
        postform = TestPostForm3
        if postform.is_valid():
            postform.save()
        else:
            logger.debug('---------------form is fail---------------')
            logger.debug(postform.errors.as_json())
    

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
    #paginate_by = 10

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