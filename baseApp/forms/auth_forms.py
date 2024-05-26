from typing import Any
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from ..models import CustomUser

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
            "password2"
        )

class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'