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
import django
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog
from . import views
from django.contrib import admin
from .tokens import user_tokenizer
from .views import contactView, successView, volunteerView

# from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("signup", views.signup, name="signup"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("reset-password-confirmation", views.reset_confirmation_sent, name='password_reset_confirm_sent'),
    path("reset-password", views.reset_password, name="reset-password"),
    path("email-test1", views.email_test1, name="email-test1"),
    path("email-test2", views.email_test2, name="email-test2"),
    path('confirm-email', views.account_activation_sent, name='confirm_email_sent'),
    path('map_page', views.map_page, name='map_page'),
    path('profile-edit', views.profile_edit, name='profile_edit'),
    path('profile-view', views.profile_view, name='profile-view'),
    path('my-posts', views.my_posts, name='my-posts'),
    path('new-dpost', views.new_dpost, name='new_dpost'),
    path('new-rpost', views.new_rpost, name='new_rpost'),

    path('contact', contactView, name='contact'),
    path('success', successView, name='success'),
    path('volunteer', volunteerView, name='volunteer'),

    path('<single_slug>/delete/', views.delete, name='delete'),
    path('<single_slug>/edit-rpost/', views.edit_rpost, name='edit-rpost'),
    path('<single_slug>/edit-dpost/', views.edit_dpost, name='edit-dpost'),
    path("<single_slug>", views.single_slug, name="single_slug"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# If you already have a js_info_dict dictionary, just add
# 'recurrence' to the existing 'packages' tuple.
js_info_dict = {
    'packages': ('recurrence', ),
}

# jsi18n can be anything you like here
urlpatterns += [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict),
]
