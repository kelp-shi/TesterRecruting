from django import forms
from ..db.application.app_models import TestPost, JoinRequest
from ..db.application.TestTypeSubclass import *

class TestPostForm(forms.ModelForm):
    """
    テストポストフォームクラス

    Note:
        テストポストのフォームクラス
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TestPost
        fields = [
            'PostName',
            'Discription',
            'RecrutingNum',
            'ApplyNum',
            'TestType',
            'TestTypeSubcls',
            'RecrutingPeriodSt',
            'RecrutingPeriodEnd',
            'TestStart',
            'TestEnd']
        
class ApplyForm(forms.ModelForm):
    class Meta:
        model = JoinRequest
        fields = ['AppealText']