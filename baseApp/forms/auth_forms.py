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
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

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

class ProfileEditForm(forms.Form):
    """
    ユーザー情報更新フォーム
    """
    class Meta:
        model = CustomUser
        fields = (
            'UserBirth',
            'UserGender',
            'profile_img'
        )