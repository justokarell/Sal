from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import InfoPrompt, CustomUser, Profile, Availability, DonorPost, RecipientPost, DonorRepeatingPost, RecipientRepeatingPost
from .forms import CustomUserChangeForm, CustomUserCreationForm 
# ProfileForm, DonorPostForm, DonorRepeatingPostForm
from address.models import AddressField
from address.forms import AddressWidget
# Register your models here.

admin.site.register(InfoPrompt)

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('post_day','start_hour','end_hour','assigned_post')

admin.site.register(Availability, AvailabilityAdmin)

class ProfileAdmin(admin.ModelAdmin):
    # fields = ['org_name', 'org_email','org_phone','org_address','image','org_desc','org_role']
    list_display = ('user','org_name','org_role','org_email','org_phone','org_address','org_city','org_state','org_zipcode','org_country','image','org_desc')

admin.site.register(Profile, ProfileAdmin)

class DonorPostAdmin(admin.ModelAdmin):
    fields = ('post_creator','post_title', 'post_org_name','post_org_phone','post_org_email','post_org_address','post_org_city',
        'post_org_state','post_org_zipcode','post_org_country','post_image','post_desc', 'post_begin_date', 'post_end_date',
         'post_recurring', 'recurrences','post_deliver')
# 'post_avail',
admin.site.register(DonorPost, DonorPostAdmin)

# class DonorRepeatingPostAdmin(admin.ModelAdmin):
#     list_display = ('post_creator','post_title', 'post_org_name','post_org_phone','post_org_email','post_org_address','post_org_city',
#         'post_org_state','post_org_zipcode','post_org_country','post_image','post_desc', 'post_begin_date', 'post_end_date',
#         'post_recurring','post_deliver','recurrences')

# admin.site.register(DonorRepeatingPost, DonorRepeatingPostAdmin)


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

