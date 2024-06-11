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