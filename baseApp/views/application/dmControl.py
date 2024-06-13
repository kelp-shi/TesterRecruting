from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from baseApp.db.application.dm_models import DirectMassage
from baseApp.forms.dm_forms import MessageForm
from baseApp.models import CustomUser

class ThreadListView(LoginRequiredMixin, View):
    """
    スレッドリストビュークラス
    """
    def get(self, request):
        # ログインユーザーに関連するすべてのメッセージを取得
        messages = DirectMassage.objects.filter(sender=request.user) | DirectMassage.objects.filter(receiver=request.user)
        # メッセージを相手ユーザーでグループ化
        threads = {}
        # 取得したメッセージを作成日で並べ替える
        for dm in messages.order_by('Created_at'):
            other_user = dm.receiver if dm.sender == request.user else dm.sender
            if other_user not in threads:
                threads[other_user] = []
            threads[other_user].append(dm)

        return render(request, 'messaging/thread_list.html', {'threads': threads})

class MessageDetailView(LoginRequiredMixin, View):
    """
    ダイレクトメッセージ詳細画面
    """
    def get(self, request, user_id):
        other_user = get_object_or_404(CustomUser, id=user_id)
        form = MessageForm()
        messages = DirectMassage.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=request.user))
        ).order_by('Created_at')

        # メッセージの既読ステータスを更新
        messages.filter(receiver=request.user).update(read=True)

        return render(request, 'messaging/message_detail.html', {'form': form, 'messages': messages, 'other_user': other_user})

    def post(self, request, user_id):
        other_user = get_object_or_404(CustomUser, id=user_id)
        form = MessageForm(request.POST)
        if form.is_valid():
            dm = form.save(commit=False)
            dm.sender = request.user
            dm.receiver = other_user
            dm.save()
            return redirect('message_detail', user_id=user_id)

        messages = DirectMassage.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=request.user))
        ).order_by('Created_at')

        # メッセージの既読ステータスを更新
        messages.filter(receiver=request.user).update(read=True)

        return render(request, 'messaging/message_detail.html', {'form': form, 'messages': messages, 'other_user': other_user})
