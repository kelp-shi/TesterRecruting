from django.db import models

class Thread(models.Model):
    """
    スレッドクラス
    """
    participants = models.ManyToManyField('baseApp.TestPost', related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Thread {self.id}'
    
class DirectMassage(models.Model):
    """
    ダイレクトメッセージクラス
    """
    #送り主
    sender = models.ForeignKey('baseApp.TestPost', on_delete=models.CASCADE, related_name='sent_messages')
    #受取人
    recipient = models.ForeignKey('baseApp.TestPost', on_delete=models.CASCADE, related_name='received_messages')
    #スレッド
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    #DM内容
    text = models.TextField(verbose_name="メッセージ内容")
    #作成日
    
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.sender}: {self.text[:30]}'

