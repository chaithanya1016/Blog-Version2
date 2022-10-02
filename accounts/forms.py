from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField,UserChangeForm

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        #self.helper.form_action = reverse_lazy('index')
        #self.helper.form_method = 'GET'
        #self.helper.add_input(Submit('submit', 'Submit'))
    #email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'validate',}))
    password2 = forms.CharField(label='Confirm Password(Again)', widget = forms.PasswordInput)
    class Meta:
        model = User
        #email = { 'required': True }
        fields = ['username','first_name', 'last_name', 'email']
        labels = {'email' : 'Email'}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput())
    password = forms.CharField(label=("Password"))


class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'last_login']
        labels = {'email' : 'Email'}

class EditAdminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'
        labels = {'email' : 'Email'}
