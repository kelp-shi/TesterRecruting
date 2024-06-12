from typing import Any
from django.db import models
from .TestTypeSubclass import TestTypeSubclass
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

class TestPost (models.Model):
    """テストタスククラス
    
    Note:
        募集するテストのクラス

    Attributes:
        id(int):テストタスクのID
        PostName(str):テストタスクの名前
        Discription(str):テスト説明
        RecrutingNum(int):募集人数
        ApplyNum(int):応募数
        TestType(int):テスト種類
        TestTypeSubcls(str):テスト細分類
        RecrutingPeriodFlg(bool):募集有無フラグ
        RecrutingPeriodSt(DateTime):募集開始日
        RecrutingPeriodEnd(DateTime):募集終了日
        TestStart(DateTime):テスト開始日
        TestEnd(DateTime):テスト終了日
        DelFlg(bool):削除フラグ
        CreateUser(ForeignKey):投稿者
        
    実装予定:
        タスク単価
        タスク合価
    """

    TEST_TYPE_CHOICE = (
        (1, 'Game'),
        (2, 'Application')
    )
    #id(str):テストタスクのID
    id = models.BigIntegerField(unique=True, blank=True, primary_key=True)
    #PostName(str):テストタスクの名前
    PostName = models.CharField('Post Name', max_length=100)
    #Discription(str):テスト説明
    Discription = models.TextField('Discription', max_length=5000)
    #RecrutingNum(int):募集人数
    RecrutingNum = models.IntegerField('Recruting People', validators=[MinValueValidator(1)])
    #ApplyNum(int):応募数
    ApplyNum = models.IntegerField('Apply People', validators=[MinValueValidator(1)])
    #TestType(int):テスト種類
    TestType = models.IntegerField('Test Type', choices=TEST_TYPE_CHOICE, default=1)
    #TestTypeSubcls(str):テスト細分類
    TESTTYPE_CHOICES = [(t.value, t.name) for t in TestTypeSubclass]
    TestTypeSubcls = models.CharField(choices=TESTTYPE_CHOICES, default=TestTypeSubclass.ART_AND_DESIGN, max_length=100)
    #RecrutingPeriodFlg(bool):募集有無フラグ
    RecrutingPeriodFlg = models.BooleanField('Recruting presence or absence Flag', default=True)
    #RecrutingPeriodSt(DateTime):募集開始日
    RecrutingPeriodSt = models.DateTimeField('Recruting Period Start')
    #RecrutingPeriodEnd(DateTime):募集終了日
    RecrutingPeriodEnd = models.DateTimeField('Recruting Period End')
    #TestStart(DateTime):テスト開始日
    TestStart = models.DateTimeField('Test Start')
    #TestEnd(DateTime):テスト終了日
    TestEnd = models.DateTimeField('Test End')
    #DelFlg(bool):削除フラグ
    DelFlg = models.BooleanField('Delete Flag', default=False)
    #CreateUser(ForeignKey):投稿者
    CreateUser = models.ForeignKey('baseApp.CustomUser', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.PostName
    

class JoinRequest(models.Model):
    """
    申し込みモデルクラス
    """
    #送り主
    Sender = models.ForeignKey('baseApp.CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    #テスト
    subjectTest = models.ForeignKey('baseApp.TestPost', on_delete=models.CASCADE, blank=True, null=True)
    #アピール文章
    AppealText = models.TextField('Appeal', max_length=5000)
    #投稿日
    create_dt = models.DateTimeField(auto_now_add=True)
