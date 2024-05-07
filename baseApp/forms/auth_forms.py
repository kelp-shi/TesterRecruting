from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from ..models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "UserBirth",
            "UserGender",
            "profile_img",
            "age",
        ]