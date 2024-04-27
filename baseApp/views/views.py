from django import views
from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from ..models.models import TestPost
from ..forms import TestPostForm
import datetime

# Create your views here.

class createTask(views.View):
    """
    新規テストポストの作成
    """
    def get(self, request):
        """
        GETリクエスト時の新規テスト作成処理
        """
        #新規オブジェクト作成
        post = TestPost()

        #GETリクエスト時の処理
        form = TestPostForm(isinstance = post)
        return render(request, 'form_html_link', {'form' : form}) #修正必須(HTML_NAME入力)
    
    def post(self, request):
        """
        POSTリクエスト時の新規テスト保存処理
        """
        #新規オブジェクト作成
        post = TestPost()

        #POSTリクエスト時の処理
        form = TestPostForm(request.POST, isinstance = post)

        #バリデーションチェック
        if form.is_valid():
            #保存処理
            post = form.save(commit = False)
            post.save()
            return redirect('net_html_link') #修正必須(HTML_NAME入力)
        
        #バリデーション不可時に再度フォーム表示
        return render(request, 'form_html_link', {'form' : form}) #修正必須(HTML_NAME入力)

class TestPostSearchView(ListView):
    """
    テストポストの表示・検索
    Note:
    部分一致可:大小区別なし
    募集期日検索（期日が近い）
    募集期日検索（期日が遠い）
    テスト期日検索（期日が近い）
    テスト期日検索（期日が遠い）
    """
    model = TestPost
    template_name = ''
    context_object_name = 'testposts'
    # ページネーション
    paginate_by = 10

    @method_decorator(cache_page(60))  # キャッシュを60秒間有効にする
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by')
        now = datetime.datetime.now()

        if query:
            # テストポストの全件取得（条件：募集フラグ==True, 削除フラグ==Falese）
            queryset = TestPost.objects.filter(RecrutingPeriodFlg=True, DelFlg=False).order_by('id')
        else:
            # 名称検索（部分一致可:大小区別なし）
            queryset = TestPost.objects.filter(PostName__icontains=query)
        
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
                queryset = TestPost.objects.none()  # 何も返さない場合は空のクエリセットを返す

        return queryset
        
    def get_context_data(self, **kwargs):
        """
        検索結果が空の場合
        """
        context = super().get_context_data(**kwargs)
        if not self.object_list.exists():
            context['no_results_message'] = '検索結果がありません。'
        return context

