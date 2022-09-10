from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from .models import Article, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']

#Add Article
class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


#Article Update
class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','slug','overview','article_image','author','category','content','status']


