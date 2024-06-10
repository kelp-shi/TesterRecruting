#utility views
import os
import io
import logging
import random, string
from PIL import Image
from baseApp.models import CustomUser
from django.core.signing import dumps
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

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

def randomString():
    """
    ランダムな文字列を作成
    """
    randomText = random.choice(string.ascii_letters + string.digits)
    return randomText

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

def errorEmailSender(self, errorMsg):
    """
    管理者へエラーメッセージを送付する
    """
    user = CustomUser.objects.get(self)
    current_site = get_current_site(self.request)
    domain = current_site.domain
    context = {
        'protocol': self.request.scheme,
        'domain': domain,
        'errorMsg': errorMsg,
    }
    # サブジェクト
    subject = render_to_string('admin/email/subject.txt', context)
    # メッセージ
    message = render_to_string('admin/email/message.txt', context)
    user.email_user(subject, message)


        


