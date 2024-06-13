from django.db import models
    
class DirectMassage(models.Model):
    """
    ダイレクトメッセージクラス

    Attributes:
        Sender(ForeignKey):送り主
        Recipient(ForeignKey):受取人
        Thread(ForeignKey):スレッド
        Text(Text):DM内容
        Created_at(DateTime):作成日
        ReadFlg(bool):既読有無フラグ
    """
    #Sender(ForeignKey):送り主
    Sender = models.ForeignKey('baseApp.TestPost', on_delete=models.CASCADE, related_name='sent_messages')
    #Recipient(ForeignKey):受取人
    Recipient = models.ForeignKey('baseApp.TestPost', on_delete=models.CASCADE, related_name='received_messages')
    #Text(Text):DM内容
    Text = models.TextField(verbose_name="メッセージ内容")
    #Created_at(DateTime):作成日
    Created_at = models.DateTimeField(auto_now_add=True)
    #ReadFlg(bool):既読有無フラグ
    ReadFlg = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender}: {self.text[:30]}'

