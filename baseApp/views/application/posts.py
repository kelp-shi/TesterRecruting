from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy, reverse

from baseApp.db.application.app_models import TestPost

from baseApp.views.dm.dmControl import createDirectMsgforApply
from baseApp.forms.application_forms import *
from baseApp.views.utillity import randomNumver
from baseApp.models import CustomUser

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

    #@method_decorator(cache_page(60))  # キャッシュを60秒間有効にする
    #def dispatch(self, *args, **kwargs):
    #    return super().dispatch(*args, **kwargs)
    
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
    context_object_name = 'postdetail'
    #テストポストデータ取得
    def get_context_data(self, **kwargs):
        #存在確認フラグ
        existenceFlg = False
        context = super().get_context_data(**kwargs)

        #存在存在チェック
        existenceUser = JoinRequest.objects.filter(Q(SubjectTest=self.kwargs['pk']) & (Q(Sender=self.request.user) & Q(authorizationFlg=False)))

        #既に申請されていた場合、存在確認フラグをTrueに
        if existenceUser.exists():
            existenceFlg = True

        context['id'] = self.kwargs['pk']
        context['existenceFlg'] = existenceFlg
        return context

    #accessユーザによってテンプレート切り替え
    def get_template_names(self):
        accessUser = self.request.user
        if self.object.CreateUser == accessUser:
            return ['app/createUser_detail.html']
        else:
            return ['app/detail.html']
        
class ApplyTask(FormView):
    """
    申請クラス

    Note:詳細ページで応募ボタン押下時に呼び出される
    """
    def get(self, request, pk):
        form = ApplyForm()
        return render(request, 'app/applytask.html', {'form':form})

    def post(self, request, pk):
        form = ApplyForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(TestPost, pk=pk)
            join_request = form.save(commit=False)
            join_request.Sender = request.user
            join_request.SubjectTest = post
            join_request.save()
            return redirect(reverse('baseApp:detail', kwargs={'pk': pk}))
        return render(request, 'app/applytask.html', {'form': form})
    
class Authorization(FormView, ListView):
    """
    テストユーザー認可クラス ※未実装

    Note:申請を送ったユーザーを認証する
    """
    template_name = 'app/authorization.html'
    context = 'authorization'
    form_class = AuthorizationForm

    def get_queryset(self):
        testid = self.kwargs['pk']
        logger.info('get query -- ')
        # JoinRequestからSubjectTest_idが一致するSender情報を取得
        sender_ids = JoinRequest.objects.filter(SubjectTest_id=testid, authorizationFlg = False).values_list('Sender_id', flat=True)
        # Sender情報を元にCustomUserを検索
        return CustomUser.objects.filter(id__in=sender_ids)

    def get_context_data(self, **kwargs):
        testid = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        # TestPostオブジェクトを取得してコンテキストに追加
        subject_test = get_object_or_404(TestPost, pk=testid)
        context['subject_test'] = subject_test
        context['custom_users'] = self.get_queryset()
        return context

    #認証押下時の処理
    def post(self, request, *args, **kwargs):
        testid = self.kwargs['pk']
        join_requests = JoinRequest.objects.filter(SubjectTest_id=testid, authorizationFlg = False)
        sender_ids = JoinRequest.objects.filter(SubjectTest_id=testid, authorizationFlg = False).values_list('Sender_id', flat=True)
        
        for join_request in join_requests:
            if str(join_request.Sender_id) in request.POST.getlist('select'):
                join_request.authorizationFlg = True
                join_request.save()
                
                createDirectMsgforApply(self, request, self.get_queryset(), sender_ids)

        return redirect(reverse('baseApp:detail', kwargs={'pk': testid}))
