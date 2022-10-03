from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from .models import Comment, Article
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout, Fieldset, Submit

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']

#Add Article
class AddArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        #self.helper.form_action = reverse_lazy('index')
        #self.helper.form_method = 'GET'
        #self.helper.add_input(Submit('submit', 'Submit'))
    class Meta:
        model = Article
        fields = '__all__'


#Article Update
class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','slug','overview','article_image','author','category','content','status']


