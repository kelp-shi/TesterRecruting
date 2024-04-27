from typing import Any
from django.db import models
from .TestTypeSubclass import TestTypeSubclass


class TestPost (models.Model):
    """テストタスククラス
    
    Note:
        募集するテストのクラス

    Attributes:
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
    """
    #PostName(str):テストタスクの名前
    PostName = models.CharField('Post Name', max_length=100)

    #Discription(str):テスト説明
    Discription = models.TextField('Discription', max_length=5000)

    #RecrutingNum(int):募集人数
    RecrutingNum = models.IntegerField('Recruting People', max_length=3)

    #ApplyNum(int):応募数
    ApplyNum = models.IntegerField('Apply People', max_length=3)

    #TestType(int):テスト種類
    TestType = models.IntegerChoices(initial=1,)
    TEST_TYPE = ((1, 'Game'),(2, 'Application'))

    #TestTypeSubcls(str):テスト細分類
    TESTTYPE_CHOICES = [(t.value, t.name) for t in TestTypeSubclass]
    TestTypeSubcls = models.CharField(choices=TESTTYPE_CHOICES, default=TestTypeSubclass.ART_AND_DESIGN)

    #RecrutingPeriodFlg(bool):募集有無フラグ
    RecrutingPeriodFlg = models.BooleanField('Recruting presence or absence Flag', default=False)

    #RecrutingPeriodSt(DateTime):募集開始日
    RecrutingPeriodSt = models.DateTimeField('Recruting Period Start')

    #RecrutingPeriodEnd(DateTime):募集終了日
    RecrutingPeriodEnd = models.DateTimeField('Recruting Period End')

    #TestStart(DateTime):テスト開始日
    TestStart = models.DateTimeField('Test Start')

    #TestEnd(DateTime):テスト終了日
    TestEnd = models.DateTimeField('Test End')

    #DelFlg(bool):削除フラグ
    DelFlg = models.BooleanField('Delete Flag')

    def __str__(self):
        return self.PostName


