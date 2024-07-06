from django.db import models
from baseApp.models import CustomUser

class DmRoom(models.Model):
    """
    DMルームクラス

    Attributes:
        Member(ManyToMany):Dm参加メンバー
        create_at(DateTime):作成日
        delFlg(Bool):削除フラグ
    """

    Member = models.ManyToManyField(CustomUser, related_name='room')
    create_at = models.DateTimeField(auto_now_add=True)
    delFlg = models.BooleanField(default=False)

class Massage(models.Model):
    """
    メッセージクラス

    Attributes:
        Sender(ForeignKey):送り主
        Recipient(ForeignKey):受取人
        Thread(ForeignKey):スレッド
        Text(Text):DM内容
        Created_at(DateTime):作成日
        ReadFlg(bool):既読有無フラグ
    """
    Room = models.ForeignKey(DmRoom, on_delete=models.CASCADE, related_name='related_room')
    #Sender(ForeignKey):送り主
    Sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    #Recipient(ForeignKey):受取人
    #Recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    #Text(Text):DM内容
    Text = models.TextField(verbose_name="メッセージ内容")
    #Created_at(DateTime):作成日
    Created_at = models.DateTimeField(auto_now_add=True)
    #ReadFlg(bool):既読有無フラグ
    ReadFlg = models.BooleanField(default=False)

    #def __str__(self):
    #    return self.Sender