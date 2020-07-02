"""Sal_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from main.tokens import user_tokenizer
from main import views

urlpatterns = [
    path('', include('main.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('confirm-email/<str:user_id>/<str:token>/', views.ConfirmRegistrationView.as_view(), name='confirm_email'),
    path('reset-password', auth_views.PasswordResetView.as_view(template_name='main/reset_password.html',
      html_email_template_name='main/reset_password_email.html',
      success_url=settings.LOGIN_URL,
      token_generator=user_tokenizer),
      name='reset_password'),
    path(
        'reset-password-confirmation/<str:uidb64>/<str:token>/',
        auth_views.PasswordResetConfirmView.as_view(
        template_name='main/reset_password_update.html', 
        post_reset_login=True,
        post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
        token_generator=user_tokenizer,
        success_url=settings.LOGIN_REDIRECT_URL),
        name='password_reset_confirm'),

    # path('admin/', include('admin.site.urls')),
    
]
