from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import InfoPrompt, CustomUser, CustomUserManager
 
# Register your models here.

admin.site.register(InfoPrompt)
admin.site.register(CustomUser)


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
    

