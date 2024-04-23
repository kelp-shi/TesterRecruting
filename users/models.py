from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from baseApp.models import TestPost

from datetime import date

class Gender(models.TextChoices):
    """
    性別選択用クラス

    Note:カスタムユーザークラスで使用する性別選択用クラス
    Attributes:男性、女性、その他
    """
    MAN     = 'Man'
    WOMEN   = 'Women'
    OTHER   = 'Other'

class CustomUser (AbstractUser, PermissionsMixin):
    """
    カスタムユーザークラス

    Note:ユーザー情報のクラス

    Attributes:
        AccountName(str):アカウント名(IDとは異なりユーザーが設定できる)
        UserBirth(dt):ユーザー誕生日
        UserGender(str):ユーザー性別
        RunningTest(mtm):実行中テストタスク(テストの外部キーを使用)
        DoneTest(mtm):完了テスト(テストの外部キーを使用)
    """
    #AccountName(str):アカウント名(IDとは異なりユーザーが設定できる)
    AccountName = models.CharField(max_length=100, required=True)

    #UserBirth(dt):ユーザー誕生日
    UserBirth = models.DateField(blank=True, null=True)

    #UserGender(str):ユーザー性別
    GENDER_CHOICES = [(g.value, g.name) for g in Gender]
    UserGender = models.CharField(max_length=50, choices=GENDER_CHOICES, default=Gender.OTHER, blank=True, null=True)

    #RunningTest(mtm):実行中テストタスク(テストの外部キーを使用)
    RunningTest = models.ManyToManyField(TestPost, related_name='running_tests')

    #DoneTest(mtm):完了テスト(テストの外部キーを使用)
    DoneTest = models.ManyToManyField(TestPost, related_name='done_tests')

    #年齢計算
    def ageMath(self):
        today = date.today()
        #現在月日が記入月日より過ぎていれば0、以前であれば-1
        age = today.year - self.UserBirth.year - ((today.month, today.day) < (self.UserBirth.month, self.UserBirth.day))
        return age

    def __str__(self):
        return self.AccountName

