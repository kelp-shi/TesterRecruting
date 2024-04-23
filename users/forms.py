from django import forms
from users.models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['AccountName', 'UserBirth', 'UserGender']