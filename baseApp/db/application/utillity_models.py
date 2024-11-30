from django.db import models
from django.urls import reverse

class BannerImg(models.Model):
    """
    index.htmlのBanner
    """
    bannerTitle = models.CharField(max_length=255)
    bannerImg = models.ImageField(upload_to='baseApp/contents/org/banner', null=False)
    activeFlg = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.activeFlg:
            BannerImg.objects.filter(activeFlg=True).update(activeFlg=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.bannerTitle
    
class news(models.Model):
    """
    news
    """
    NewsTitle = models.CharField(max_length=150)
    Newsinner = models.TextField(max_length=5000)
    CreateUser = models.ForeignKey('baseApp.CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    RelatedBanner = models.ForeignKey(BannerImg, blank=True, null=True, on_delete=models.CASCADE)
    Create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.NewsTitle
    
    def get_absolute_url(self):
        return reverse('baseApp:newsDetail', args=[str(self.id)])