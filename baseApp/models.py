from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser, UserManager, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from testerRecruting.settings import DEFAULT_PROFILE_IMAGE_PATH
from baseApp.db.application.app_models import TestPost
from datetime import date
from django.utils import timezone

class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class Gender(models.TextChoices):
    """
    性別選択用クラス

    Note:カスタムユーザークラスで使用する性別選択用クラス
    Attributes:男性、女性、その他
    """
    MAN     = 'Man'
    WOMEN   = 'Women'
    OTHER   = 'Other' 

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
        age(int):ユーザーの年齢
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

    #CreateTest(mtm):作成済みテスト
    MyTest = models.ManyToManyField(TestPost, related_name='create_user', blank=True)

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
    profile_img = models.ImageField(upload_to='baseApp/images/user/profile/', blank=True, null=True, default=DEFAULT_PROFILE_IMAGE_PATH)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
            
    #年齢(int):ユーザーの年齢
    age = models.IntegerField(blank=True, null=True)

    objects = CustomUserManager()

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
        age_result = today.year - self.UserBirth.year - ((today.month, today.day) < (self.UserBirth.month, self.UserBirth.day))
        self.age = age_result
    
    #保存メソッド（年齢計算結果をインサート）
    def save(self, *args, **kwargs):
        if self.UserBirth:
            today = date.today()
            # 現在の年から生年月日の年を引いて年齢を計算
            self.Age = today.year - self.UserBirth.year - ((today.month, today.day) < (self.UserBirth.month, self.UserBirth.day))

        super().save(*args, **kwargs)