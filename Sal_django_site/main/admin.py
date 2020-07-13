from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import InfoPrompt, CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.

admin.site.register(InfoPrompt)


class InfoPromptAdmin(admin.ModelAdmin):
    fields = [
        'org_name',
        'org_email'
    ]
    fieldsets = (
        ("Contact Info", {
            "fields": ("Organization Name", "Email Address"
                
            ),
        }),
    )
    
class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('org_name', 'address')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'org_name', 'address', 'phone', 'is_staff')
    search_fields = ('email', 'org_name', 'address', 'phone',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)