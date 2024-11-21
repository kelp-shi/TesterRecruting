from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from ..models import CustomUser
from django import forms

class SignUpForm(UserCreationForm):
    """
    ユーザー登録フォーム
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].initial = 'username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].initial = 'email'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].initial = 'Password'
        self.fields['password2'].initial = 'Confirm Password'

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

class SignInForm(AuthenticationForm):
    """
    ログインフォーム
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class ProfileEditForm(forms.ModelForm):
    """
    ユーザー情報更新フォーム
    """

    class Meta:
        model = CustomUser
        fields = (
            'UserBirth',
            'UserGender',
            'profile_img',
            'email_for_test',
            'bio_text'
        )
    
    widgets = {
        'UserBirth': forms.DateInput(
            attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'format': 'Y-m-d'}),
        'UserGender': forms.Select( choices=CustomUser.GENDER_CHOICES, attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
    }