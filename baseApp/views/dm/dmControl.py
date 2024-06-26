from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from baseApp.db.application.dm_models import DmRoom, Massage
from baseApp.models import CustomUser
from baseApp.forms.dm_forms import MessageForm
from django.http import Http404
import logging

logger = logging.getLogger(__name__)

class ThreadListView(LoginRequiredMixin, View):
    """
    スレッドリストビュークラス
    """
    def get(self, request):
        # ログインユーザーがメンバーに含まれているDmRoomを取得
        rooms = DmRoom.objects.filter(Member=request.user)
        return render(request, 'dm/threadList.html', {'rooms': rooms})

class MessageDetailView(LoginRequiredMixin, View):
    def get(self, request, room_id):
        logger.info(room_id)
        room = get_object_or_404(DmRoom, id=room_id)

        if request.user not in room.Member.all():
            raise Http404

        form = MessageForm()
        messages = Massage.objects.filter(Room=room).order_by('Created_at')

        messages.filter(Sender=request.user).update(ReadFlg=True)

        return render(request, 'dm/message_detail.html', {'form': form, 'messages': messages, 'room': room})

    def post(self, request, room_id):
        room = get_object_or_404(DmRoom, id=room_id)

        if request.user not in room.Member.all():
            raise Http404
        
        form = MessageForm(request.POST)
        if form.is_valid():
            dm = form.save(commit=False)
            dm.Sender = request.user
            dm.Room = room
            dm.save()
            return redirect('baseApp:message_detail', room_id=room_id)

        messages = Massage.objects.filter(Room=room).order_by('Created_at')

        # メッセージの既読ステータスを更新
        messages.filter(Sender=request.user).update(ReadFlg=True)

        return render(request, 'dm/message_detail.html', {'form': form, 'messages': messages, 'room': room})
    
def createDirectMsgforApply(self, request, member1, member2, msg):
    """
    認証DM新規作成メソッド

    Note:認可されたユーザーとの間にDMを開く
    member1: 募集者
    member2: 申込者
    """
    #logger.debug(member1 + ":" + member2 + ":" + msg)

    creatuser = CustomUser.objects.get(id=member1)
    senduser = CustomUser.objects.get(id=member2)
    # DmRoom作成
    dmRoom = DmRoom.objects.create()
    dmRoom.Member.add(creatuser)
    dmRoom.Member.add(senduser)
    dmRoom.save()

    # Message作成
    message = Massage.objects.create(
        Room=dmRoom,
        Sender=creatuser,
        Text=msg
    )
    message.save()

    
    