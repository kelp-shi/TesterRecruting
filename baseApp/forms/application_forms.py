from django import forms
from ..db.application.app_models import TestPost, JoinRequest
from ..db.application.TestTypeSubclass import *
import datetime

class TestPostForm(forms.ModelForm):
    """
    テストポストフォームクラス

    Note:
        テストポストのフォームクラス
    """
    #人数選択範囲
    PEOPLE_CHOICES = [(people, people) for people in range(101)]
    ApplyPeople = forms.ChoiceField(choices=PEOPLE_CHOICES, label='人数')
    RecrutingNumPeople = forms.ChoiceField(choices=PEOPLE_CHOICES, label='人数')

    #日付選択範囲
    current_year = datetime.datetime.now().year
    YEAR_CHOICES = [(year, year) for year in range(1950, current_year + 1)]
    MONTH_CHOICES = [(month, month) for month in range(1, 13)]
    DAY_CHOICES = [(day, day) for day in range(1, 32)]

    recruiting_period_st_year = forms.ChoiceField(choices=YEAR_CHOICES, label='開始年')
    recruiting_period_st_month = forms.ChoiceField(choices=MONTH_CHOICES, label='開始月')
    recruiting_period_st_day = forms.ChoiceField(choices=DAY_CHOICES, label='開始日')
    
    recruiting_period_end_year = forms.ChoiceField(choices=YEAR_CHOICES, label='終了年')
    recruiting_period_end_month = forms.ChoiceField(choices=MONTH_CHOICES, label='終了月')
    recruiting_period_end_day = forms.ChoiceField(choices=DAY_CHOICES, label='終了日')

    test_start_year = forms.ChoiceField(choices=YEAR_CHOICES, label='テスト開始年')
    test_start_month = forms.ChoiceField(choices=MONTH_CHOICES, label='テスト開始月')
    test_start_day = forms.ChoiceField(choices=DAY_CHOICES, label='テスト開始日')
    
    test_end_year = forms.ChoiceField(choices=YEAR_CHOICES, label='テスト終了年')
    test_end_month = forms.ChoiceField(choices=MONTH_CHOICES, label='テスト終了月')
    test_end_day = forms.ChoiceField(choices=DAY_CHOICES, label='テスト終了日')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.datetime.now()
        self.fields['ApplyPeople'].initial = 0
        self.fields['RecrutingNumPeople'].initial = 0
        self.fields['recruiting_period_st_year'].initial = today.year
        self.fields['recruiting_period_st_month'].initial = today.month
        self.fields['recruiting_period_st_day'].initial = today.day
        self.fields['recruiting_period_end_year'].initial = today.year
        self.fields['recruiting_period_end_month'].initial = today.month
        self.fields['recruiting_period_end_day'].initial = today.day
        self.fields['test_start_year'].initial = today.year
        self.fields['test_start_month'].initial = today.month
        self.fields['test_start_day'].initial = today.day
        self.fields['test_end_year'].initial = today.year
        self.fields['test_end_month'].initial = today.month
        self.fields['test_end_day'].initial = today.day
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TestPost
        fields = [
            'PostName',
            'Discription',
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

class TestCloseForm(forms.ModelForm):
    close = forms.BooleanField(required=True, label="クローズ")

    class Meta:
        model = TestPost
        fields = []