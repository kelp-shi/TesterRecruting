from django.contrib.auth.models import AbstractUser, PermissionsMixin,AbstractBaseUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from baseApp.db.application.app_models import TestPost
from datetime import date
from django.utils import timezone

class Gender(models.TextChoices):
    """
    性別選択用クラス

    Note:カスタムユーザークラスで使用する性別選択用クラス
    Attributes:男性、女性、その他
    """
    MAN     = 'Man'
    WOMEN   = 'Women'
    OTHER   = 'Other'

#class CustomUser (AbstractUser):
#    """
#    カスタムユーザークラス
#
#    Note:ユーザー情報のクラス
#
#    Attributes:
#        username(str):アカウント名(IDとは異なりユーザーが設定できる)
#        email(email):Eメール
#        UserBirth(dt):ユーザー誕生日
#        UserGender(str):ユーザー性別
#        RunningTest(mtm):実行中テストタスク(テストの外部キーを使用)
#        DoneTest(mtm):完了テスト(テストの外部キーを使用)
#    """
#    #AccountName(str):アカウント名(IDとは異なりユーザーが設定できる)
#    AccountName = models.CharField(max_length=100)
#
#    #UserBirth(dt):ユーザー誕生日
#    UserBirth = models.DateField(blank=True, null=True)
#
#    #UserGender(str):ユーザー性別
#    GENDER_CHOICES = [(g.value, g.name) for g in Gender]
#    UserGender = models.CharField(max_length=50, choices=GENDER_CHOICES, default=Gender.OTHER, blank=True, null=True)
#
#    #RunningTest(mtm):実行中テストタスク(テストの外部キーを使用)
#    RunningTest = models.ManyToManyField(TestPost, related_name='running_tests')
#
#    #DoneTest(mtm):完了テスト(テストの外部キーを使用)
#    DoneTest = models.ManyToManyField(TestPost, related_name='done_tests')
#
#    #年齢計算
#    def ageMath(self):
#        today = date.today()
#        #現在月日が記入月日より過ぎていれば0、以前であれば-1
#        age = today.year - self.UserBirth.year - ((today.month, today.day) < (self.UserBirth.month, self.UserBirth.day))
#        return age
#
#    def __str__(self):
#        return self.AccountName
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    カスタムユーザークラス

    Note:ユーザー情報のクラス

    Attributes:
        username(str):アカウント名(IDとは異なりユーザーが設定できる)
        email(email):Eメール
        UserBirth(dt):ユーザー誕生日
        UserGender(str):ユーザー性別
        RunningTest(mtm):実行中テストタスク(テストの外部キーを使用)
        DoneTest(mtm):完了テスト(テストの外部キーを使用)
        is_staff(bool):スタッフ権限
        is_active(bool):論理削除フラグ
        profile_img(img):プロフィール画像
    """

    username_validator = UnicodeUsernameValidator()

    #username(str):アカウント名
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    #email(email):Eメール
    email = models.EmailField(max_length=255, unique=True)

    #UserBirth(dt):ユーザー誕生日
    UserBirth = models.DateField(blank=True, null=True)

    #UserGender(str):ユーザー性別
    GENDER_CHOICES = [(g.value, g.name) for g in Gender]
    UserGender = models.CharField(max_length=50, choices=GENDER_CHOICES, default=Gender.OTHER, blank=True, null=True)

    #RunningTest(mtm):実行中テストタスク(テストの外部キーを使用)
    RunningTest = models.ManyToManyField(TestPost, related_name='running_tests', blank=True)

    #DoneTest(mtm):完了テスト(テストの外部キーを使用)
    DoneTest = models.ManyToManyField(TestPost, related_name='done_tests', blank=True)

    #is_staff(bool):スタッフ権限
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    #is_active(bool):論理削除フラグ
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    #profile_img(img):プロフィール画像
    profile_img = models.ImageField(upload_to='baseApp/images/user/profile/', blank=True, null=True)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        #abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    #def get_full_name(self):
    #    """
    #    Return the first_name plus the last_name, with a space in between.
    #    """
    #    full_name = "%s %s" % (self.first_name, self.last_name)
    #    return full_name.strip()

    #def get_short_name(self):
    #    """Return the short name for the user."""
    #    return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    #年齢計算
    def ageMath(self):
        today = date.today()
        #現在月日が記入月日より過ぎていれば0、以前であれば-1
        age = today.year - self.UserBirth.year - ((today.month, today.day) < (self.UserBirth.month, self.UserBirth.day))
        return age