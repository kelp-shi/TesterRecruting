#utility views
import os
import io
import logging
from PIL import Image
from baseApp.models import CustomUser
from baseApp.views.utillity import randomString
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

def imageConvert(img):
    """
    画像をjpgへ変換
    """
    # 画像を開く
    image = Image.open(img)
    # RGBに変換
    image = image.convert("RGB")
    # バイトストリームに保存
    output = io.BytesIO()
    image.save(output, format='JPEG')  # 画像フォーマットを指定
    output.seek(0)
    return ContentFile(output.getvalue(), '')

def imageNameSelect():
    """
    イメージ画像名称設定
    """
    users = CustomUser.objects.values_list('profile_img', flat=True)
    existing_file_names = [os.path.splitext(os.path.basename(user))[0] for user in users]
    
    for _ in range(2):  # 2回トライする
        name = randomString()
        if name not in existing_file_names:
            name = name + '.jpg'
            return name
    
    logger.debug('Failed to generate unique name after 2 attempts.')
    return None

def get_user_from_token(self, token):
    """
    トークン存在チェック
    """
    try:
        for user in CustomUser.objects.all():
            if check_password(token, user.reset_token):
                return user
    
    except CustomUser.DoesNotExist:
        return None

def is_token_expired(self, user):
    """
    トークン有効期限チェック
    """
    return timezone.now() > user.token_created_at + timedelta(hours=24)

        


