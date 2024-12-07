from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from baseApp.db.application.utillity_models import news

class IndexSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['baseApp:index']

    def location(self, item):
        return reverse(item)

class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return news.objects.all()

    def lastmod(self, obj):
        return obj.Create_at
    
class NewslistSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['baseApp:newslist']

    def location(self, item):
        return reverse(item)
    
class ContactSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['baseApp:contact']

    def location(self, item):
        return reverse(item)
    
class RegisterSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['baseApp:register']

    def location(self, item):
        return reverse(item)
