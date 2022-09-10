from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from webapp.models import Category,Article


class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()


class ArticleSitemap(Sitemap):
    def items(self):
        return Article.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.create

        
