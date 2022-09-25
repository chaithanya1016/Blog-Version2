from django.contrib import admin
from .models import Article, Category, Comment, Like

# Register your models here.

class CommentItemInLine(admin.TabularInline):
    model = Comment
    raw_id_fields = ['article']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title','category','author','status','article_image']
    prepopulated_fields = {'slug':('title',)}
    inlines = [CommentItemInLine]
admin.site.register(Article,ArticleAdmin)

class LikedAdmin(admin.ModelAdmin):
    list_display = ['id','user','article','value']
admin.site.register(Like, LikedAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title','slug']
    prepopulated_fields = {'slug':('title',)}
admin.site.register(Category,CategoryAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','article','name','email','body','created_at']
admin.site.register(Comment, CommentAdmin)

