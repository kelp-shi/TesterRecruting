from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from baseApp.db.application.dm_models import DmRoom, Massage
from baseApp.forms.dm_forms import MessageForm
from baseApp.models import CustomUser

class createDirectMsg():
    """
    DM新規作成クラス

    Note:認可されたユーザーとの間にDMを開く
    """

class ThreadListView(LoginRequiredMixin, View):
    """
    スレッドリストビュークラス
    """
    def get(self, request):
        # ログインユーザーがメンバーに含まれているDmRoomを取得
        rooms = DmRoom.objects.filter(Member=request.user)
        return render(request, 'dm/threadList.html', {'threads': rooms})

class MessageDetailView(LoginRequiredMixin, View):
    """
    ダイレクトメッセージ詳細画面
    """
    def get(self, request, user_id):
        other_user = get_object_or_404(CustomUser, id=user_id)
        form = MessageForm()
        messages = DirectMassage.objects.filter(
            (Q(Sender=request.user) & Q(receiver=other_user)) |
            (Q(Sender=other_user) & Q(receiver=request.user))
        ).order_by('Created_at')

        # メッセージの既読ステータスを更新
        messages.filter(receiver=request.user).update(read=True)

        return render(request, 'dm/message_detail.html', {'form': form, 'messages': messages, 'other_user': other_user})

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

        return render(request, 'dm/message_detail.html', {'form': form, 'messages': messages, 'other_user': other_user})
    