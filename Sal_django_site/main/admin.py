from django.contrib import admin
from .models import InfoPrompt
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
    

