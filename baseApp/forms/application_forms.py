from django import forms
from ..db.application.app_models import TestPost, JoinRequest
from ..db.application.TestTypeSubclass import *

class TestPostForm(forms.ModelForm):
    """
    テストポストフォームクラス

    Note:
        テストポストのフォームクラス
    """
    recruiting_period_st_year = forms.IntegerField(label='開始年', min_value=1900, max_value=2100)
    recruiting_period_st_month = forms.IntegerField(label='開始月', min_value=1, max_value=12)
    recruiting_period_st_day = forms.IntegerField(label='開始日', min_value=1, max_value=31)
    
    recruiting_period_end_year = forms.IntegerField(label='終了年', min_value=1900, max_value=2100)
    recruiting_period_end_month = forms.IntegerField(label='終了月', min_value=1, max_value=12)
    recruiting_period_end_day = forms.IntegerField(label='終了日', min_value=1, max_value=31)

    test_start_year = forms.IntegerField(label='テスト開始年', min_value=1900, max_value=2100)
    test_start_month = forms.IntegerField(label='テスト開始月', min_value=1, max_value=12)
    test_start_day = forms.IntegerField(label='テスト開始日', min_value=1, max_value=31)
    
    test_end_year = forms.IntegerField(label='テスト終了年', min_value=1900, max_value=2100)
    test_end_month = forms.IntegerField(label='テスト終了月', min_value=1, max_value=12)
    test_end_day = forms.IntegerField(label='テスト終了日', min_value=1, max_value=31)

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
            'TestTypeSubcls',]
        
class ApplyForm(forms.ModelForm):

    class Meta:
        model = JoinRequest
        fields = ['AppealText']


class AuthorizationForm(forms.ModelForm):
    select = forms.BooleanField(required=False, label='認証')

    class Meta:
        model = JoinRequest
        fields = []