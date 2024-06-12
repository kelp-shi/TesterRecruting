from django.db import models

class Thread(models.Model):
    """
    スレッドクラス

    Attributes:
        Participants(MtM):参加者
        Created_at(DateTime):作成日
    """
    #Participants(MtM):参加者
    Participants = models.ManyToManyField('baseApp.TestPost', related_name='threads')
    #Created_at(DateTime):作成日
    Created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Thread {self.id}'
    
class DirectMassage(models.Model):
    """
    ダイレクトメッセージクラス

    Attributes:
        Sender(ForeignKey):送り主
        Recipient(ForeignKey):受取人
        Thread(ForeignKey):スレッド
        Text(Text):DM内容
        Created_at(DateTime):作成日
    """
    #Sender(ForeignKey):送り主
    Sender = models.ForeignKey('baseApp.TestPost', on_delete=models.CASCADE, related_name='sent_messages')
    #Recipient(ForeignKey):受取人
    Recipient = models.ForeignKey('baseApp.TestPost', on_delete=models.CASCADE, related_name='received_messages')
    #Thread(ForeignKey):スレッド
    Thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    #Text(Text):DM内容
    Text = models.TextField(verbose_name="メッセージ内容")
    #Created_at(DateTime):作成日
    Created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.text[:30]}'

