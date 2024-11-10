from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView,CustomPasswordResetComplete,password_changed,CustomPasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


app_name = 'studentauth'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_page,name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('accountsetting/', views.accountsettings, name='accountsetting'),

    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name="registration/password_change_form.html",
    ), name="change_password"),
    path('password_changed/', views.password_changed, name='password_changed'),
    path('password_reset', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', CustomPasswordResetComplete.as_view(), name='password_reset_complete'),

]