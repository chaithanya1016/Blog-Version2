import email
from venv import create
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse


# Create your models here.

#Category
class Category(models.Model):
    title = models.CharField(max_length=15)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-title',)
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return '/%s/' % self.slug


#Article
class Article(models.Model):
    STATUS_CHOICES = (('draft','Draft'),('published','Published'))
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, unique_for_date='create')
    overview = models.TextField()
    article_image = models.ImageField(upload_to='Article_Image/')
    author = models.ForeignKey(User,related_name='blog_posts', on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, related_name="articles", on_delete=models.CASCADE, verbose_name="Category")
    content = RichTextField()
    read = models.IntegerField(default=0)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create']

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)
    

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




