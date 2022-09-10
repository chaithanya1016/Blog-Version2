
from email.headerregistry import Group
from unicodedata import name
from django.shortcuts import render,redirect, HttpResponseRedirect
from accounts.forms import SignUpForm, LoginForm, EditUserProfileForm, EditAdminProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group


# Create your views here.

#Sign Up
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account Created Succesfully')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            return redirect('login')
    else:
        form = SignUpForm()
    context = {'form':form}
    return render(request, 'accounts/signup.html', context)

#Login
def loginview(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully')
                    return HttpResponseRedirect('/accounts/dashboard/')
        else:
            form = AuthenticationForm()
        context = {'form' : form}
        return render(request, 'accounts/login.html', context)
    else:
        return HttpResponseRedirect('/accounts/dashboard/')



#logout
def logoutview(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


#Password Change with old Password
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Changed Successfully')
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/passwordchange.html', {'form': form})
    

#Password Change without old Password
@login_required
def password_change1(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Changed Successfully')
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'accounts/passwordchange1.html', {'form': form})
  
#User Profile
@login_required
def user_profile(request):
    if request.method == "POST":
        if request.user.is_superuser ==True:
            #user1 = User.objects.all
            form = EditAdminProfileForm(request.POST, instance= request.user)
            #users = User.objects.all()
        else:
            #user1 = None
            form = EditUserProfileForm(request.POST, instance=request.user)
            #users = None
            #userall = None
        if form.is_valid():
            messages.success(request, 'Profile Updated Successfully')
            form.save()
    else:
        if request.user.is_superuser == True:
            form = EditAdminProfileForm(instance=request.user)
            users = User.objects.all()
        else:
            form = EditUserProfileForm(instance=request.user)
            users = None
    return render(request, 'accounts/userprofile.html', {'form':form, 'users':users})


#User Details
def user_detail(request,id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        form = EditAdminProfileForm(instance=pi)
        return render(request, 'accounts/userdetail.html',{'form':form})
    else:
        return HttpResponseRedirect('/accounts/login/')
