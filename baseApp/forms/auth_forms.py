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

class ProfileEditForm(forms.ModelForm):
    """
    ユーザー情報更新フォーム
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['UserBirth'].widget.attrs['class'] = 'form-control'
        self.fields['UserGender'].widget.attrs['class'] = 'form-control'
        self.fields['profile_img'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = (
            'UserBirth',
            'UserGender',
            'profile_img'
        )
    
    widgets = {
        'UserBirth': forms.DateInput(attrs={'type': 'date'}),
    }