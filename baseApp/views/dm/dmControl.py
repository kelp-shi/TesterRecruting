from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from baseApp.db.application.dm_models import DmRoom, Massage
from baseApp.models import CustomUser
from baseApp.db.application.app_models import TestPost
from baseApp.forms.dm_forms import MessageForm
from django.http import Http404
import logging

logger = logging.getLogger(__name__)

class ThreadListView(LoginRequiredMixin, TemplateView):
    """
    スレッドリストビュークラス
    """
    template_name = 'dm/threadList.html'

    def get_context_data(self, **kwargs):
        # 自身の情報
        current_user = self.request.user
        context = super().get_context_data(**kwargs)
        # ログインユーザ情報
        context['user'] = current_user
        # 自身のDM
        my_dms = DmRoom.objects.filter(Member=current_user, delFlg=False)
        
        other_members = {}
        new_message = {}
        for room in my_dms:
            other_member = room.Member.exclude(id=current_user.id).first()  # 他のメンバーを取得
            my_message = Massage.objects.filter(Room=room.id).latest('Created_at')
            if other_member:
                other_members[room.id] = other_member
                new_message[room.id] = my_message

        context['rooms'] = my_dms
        context['other_members'] = other_members
        context['dmMessage'] = new_message

        return context


class MessageDetailView(LoginRequiredMixin, View):
    def get(self, request, room_id):
        logger.info(room_id)
        room = get_object_or_404(DmRoom, id=room_id)

        if request.user not in room.Member.all():
            raise Http404

        form = MessageForm()
        messages = Massage.objects.filter(Room=room).order_by('Created_at')

        messages.filter(Sender=request.user).update(ReadFlg=True)

        # Get the other user in the room
        other_user = room.Member.exclude(id=request.user.id).first()

        return render(request, 'dm/message_detail.html', {
            'form': form,
            'messages': messages,
            'room': room,
            'other_user': other_user
        })

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
    
def createDirectMsgforApply(self, request, member1, member2, testid, msg):
    """
    認証DM新規作成メソッド

    Note:認可されたユーザーとの間にDMを開く
    member1: 募集者
    member2: 申込者
    """
    #logger.debug(member1 + ":" + member2 + ":" + msg)

    creatuser = CustomUser.objects.get(id=member1)
    senduser = CustomUser.objects.get(id=member2)
    targetTest = TestPost.objects.get(id=testid)
    # DmRoom作成
    dmRoom = DmRoom.objects.create(TargetTest=targetTest)
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

def createExistingDirectMsgforApply(self, request, member1, member2, testid, msg):
    """
    DM新規作成メソッド

    Note:認可されたユーザーとの間にDMを開く
    member1: 募集者
    member2: 申込者
    """

    creatuser = CustomUser.objects.get(id=member1)
    dmRoom = DmRoom.objects.get(Member=member2, TargetTest=testid)

    # Message作成
    message = Massage.objects.create(
        Room=dmRoom,
        Sender=creatuser,
        Text=msg
    )
    message.save()

    
    