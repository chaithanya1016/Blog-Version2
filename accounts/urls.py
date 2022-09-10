from django.urls import path
from accounts import views as v1
from webapp import views as v2
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', v1.loginview, name='login'),
    path('signup/', v1.signup_view, name='signup'),
    path('dashboard/', v2.dashboard_view, name='dashboard'),
    path('logout/', v1.logoutview, name='logout'),
    path('passwordchange/', v1.password_change, name='passwordchange'),
    path('passwordchange1/', v1.password_change1, name='passwordchange1'),
    path('userprofile/', v1.user_profile, name='userprofile'),
    path('userdetail/<int:id>', v1.user_detail, name='userdetail'),
    
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change-password.html')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='reset_password'),
    
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    
    #path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='reset_password_complete'),

    #path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),

]
