from django import forms
from ..db.application.app_models import TestPost
from ..db.application.TestTypeSubclass import *

class TestPostForm(forms.ModelForm):
    """
    テストポストフォームクラス

    Note:
        テストポストのフォームクラス

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
    PostName = forms.CharField(
        label='Post Name', 
        max_length=100,
        required=True
        )

    #Discription(str):テスト説明
    Discription = forms.CharField(
        widget=forms.Textarea,
        label='Discription',
        max_length=5000,
        required=True
        )

    #RecrutingNum(int):募集人数
    RecrutingNum = forms.IntegerField(
        label='Recruting People', 
        max_value=2,
        required=True
        )

    #ApplyNum(int):応募数
    ApplyNum = forms.IntegerField(
        label='Apply People', 
        max_value=2,
        required=True
        )

    #TestType(int):テスト種類
    TestType = forms.ChoiceField(
        label='Test Type',
        initial=1,
        required=True
    )

    #TestTypeSubcls(str):テスト細分類
    TestTypeSubcls = forms.CharField(
        required=True
        )

    #RecrutingPeriodFlg(bool):募集有無フラグ
    RecrutingPeriodFlg = forms.BooleanField(
        label='Recruting presence or absence Flag',
        initial=False,
        required=True
        )

    #RecrutingPeriodSt(DateTime):募集開始日
    RecrutingPeriodSt = forms.DateTimeField(
        label='Recruting Period Start',
        required=True
        )

    #RecrutingPeriodEnd(DateTime):募集終了日
    RecrutingPeriodEnd = forms.DateTimeField(
        label='Recruting Period End',
        required=True
        )

    #TestStart(DateTime):テスト開始日
    TestStart = forms.DateTimeField(
        label='Test Start',
        required=True
        )

    #TestEnd(DateTime):テスト終了日
    TestEnd = forms.DateTimeField(
        label='Test End',
        required=True
        )

    #DelFlg(bool):削除フラグ
    DelFlg = forms.BooleanField(
        label='Delete Flag',
        initial=False,
        required=True
        )
    
class TestPostForm2(forms.ModelForm):
    class Meta:
        model = TestPost
        fields = [
            'PostName',
            'Discription',
            'RecrutingNum',
            'ApplyNum',
            'TestType',
            'TestTypeSubcls',
            'RecrutingPeriodFlg',
            'RecrutingPeriodSt',
            'RecrutingPeriodEnd',
            'TestStart',
            'TestEnd']
        
class TestPostForm3(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['PostName'].widget.attrs['class'] = 'form-control'
        self.fields['Discription'].widget.attrs['class'] = 'form-control'
        self.fields['RecrutingNum'].widget.attrs['class'] = 'form-control'
        self.fields['ApplyNum'].widget.attrs['class'] = 'form-control'
        self.fields['TestType'].widget.attrs['class'] = 'form-control'
        self.fields['TestTypeSubcls'].widget.attrs['class'] = 'form-control'
        self.fields['RecrutingPeriodFlg'].widget.attrs['class'] = 'form-control'
        self.fields['RecrutingPeriodSt'].widget.attrs['class'] = 'form-control'
        self.fields['RecrutingPeriodEnd'].widget.attrs['class'] = 'form-control'
        self.fields['TestStart'].widget.attrs['class'] = 'form-control'
        self.fields['TestEnd'].widget.attrs['class'] = 'form-control'

        class Meta:
            model = TestPost
            fields = [
                'PostName',
                'Discription',
                'RecrutingNum',
                'ApplyNum',
                'TestType',
                'TestTypeSubcls',
                'RecrutingPeriodFlg',
                'RecrutingPeriodSt',
                'RecrutingPeriodEnd',
                'TestStart',
                'TestEnd']