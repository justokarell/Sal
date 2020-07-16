from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import InfoPrompt, CustomUser, Profile
from .forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm
from address.models import AddressField
from address.forms import AddressWidget
# Register your models here.

admin.site.register(InfoPrompt)

class ProfileAdmin(admin.ModelAdmin):
    # fields = ['org_name', 'org_email','org_phone','org_address','image','org_desc','org_role']
    list_display = ('user','org_name','org_role','org_email','org_phone','org_address','org_city','org_state','org_zipcode','org_country','image','org_desc')

    # formfield_overrides = {
    #     AddressField: {
    #         'widget': AddressWidget(
    #             attrs={
    #                 'style': 'width: 300px;'
    #             }
    #         )
    #     }
    # }

admin.site.register(Profile, ProfileAdmin)

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
        (_('Personal info'), {'fields': ('your_name', 'profile')}),
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
    list_display = ('email', 'your_name',  'is_staff')
    search_fields = ('email', 'your_name' )
    ordering = ('email',)
    readonly_fields=('profile',)

admin.site.register(CustomUser, CustomUserAdmin)