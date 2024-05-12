from typing import Any
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from ..models import CustomUser

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['UserBirth'].widget.attrs['class'] = 'form-control'
        self.fields['UserGender'].widget.attrs['class'] = 'form-control'
        self.fields['profile_img'].widget.attrs['class'] = 'form-control'
        self.fields['age'].widget.attrs['class'] = 'form-control'
        
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "UserBirth",
            "UserGender",
            "profile_img",
            "age",
        )