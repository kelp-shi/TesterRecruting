from django.db import models

class BannerImg(models.Model):
    """
    index.htmlのBanner
    """
    bannerTitle = models.CharField(max_length=255)
    bannerImg = models.ImageField(upload_to='baseApp/images/org/banner', null=False)
    activeFlg = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.activeFlg:
            BannerImg.objects.filter(activeFlg=True).update(activeFlg=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.bannerTitle