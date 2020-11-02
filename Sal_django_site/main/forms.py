import os
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile, UserPost, Availability, DonorPost, RecipientPost
from .models import DAYS_OF_WEEK
# from address.forms import AddressField, AddressWidget
import django.contrib.admin.widgets
from django.utils.html import escape
from django.forms.widgets import SelectDateWidget, DateTimeInput
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.forms import ModelForm


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


AvailabilityFormset = inlineformset_factory(UserPost, Availability, fields=('post_day', 'start_hour', 'end_hour',),
                                            widgets={
    'post_day': forms.CheckboxSelectMultiple,
    'start_hour': forms.TimeInput(attrs={
        'type': 'time'
    }),
    'end_hour': forms.TimeInput(attrs={
        'type': 'time'
    })},
    extra=4,
    # can_order=True
)


class RecipientPostForm(forms.ModelForm):
    post_image = forms.ImageField(
        widget=forms.FileInput(attrs={'accept': 'image/png,.jpg'}))
    post_begin_date = forms.DateField(widget=SelectDateWidget)
    post_end_date = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = RecipientPost
        fields = ['post_title', 'post_org_name', 'post_org_phone', 'post_org_email', 'post_org_address', 'post_org_city',
                  'post_org_state', 'post_org_zipcode', 'post_org_country', 'post_desc', 'post_begin_date', 'post_image',
                  'post_end_date', 'post_deliver', 'post_recurring', 'recurrences', ]

    def clean_post_title(self):
        post_title = self.cleaned_data['post_title']
        if '@' in post_title or '-' in post_title or '|' in post_title or '&' in post_title:
           raise forms.ValidationError("Titles should not have special characters.")
        return post_title

    def clean_post_org_name(self):
        post_org_name = self.cleaned_data['post_org_name']
        if '@' in post_org_name or '-' in post_org_name or '|' in post_org_name or '&' in post_org_name:
           raise forms.ValidationError("Name should not have special characters.")
        return post_org_name

    def clean_post_org_address(self):
        post_org_address = self.cleaned_data['post_org_address']
        post_org_address = escape(post_org_address)
        return post_org_address

    def clean_post_org_country(self):
        post_org_country = self.cleaned_data['post_org_country']
        post_org_country = escape(post_org_country)
        return post_org_country    

    def clean_post_desc(self):
        post_desc = self.cleaned_data['post_desc']
        post_desc = escape(post_desc)
        return post_desc


class DonorPostForm(forms.ModelForm):
    post_image = forms.ImageField(
        widget=forms.FileInput(attrs={'accept': 'image/png,.jpg'}))
    # post_avail = forms.ModelMultipleChoiceField(queryset=Availability.objects.all(), widget=forms.SelectMultiple)
    # post_avail = inlineformset_factory(Author, Book, fields=('title',))
    post_begin_date = forms.DateField(widget=SelectDateWidget)
    post_end_date = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = DonorPost
        fields = ['post_title', 'post_org_name', 'post_org_phone', 'post_org_email', 'post_org_address', 'post_org_city',
                  'post_org_state', 'post_org_zipcode', 'post_org_country', 'post_desc', 'post_begin_date', 'post_image',
                  'post_end_date', 'post_deliver', 'post_recurring', 'recurrences', ]
    
    def clean_post_title(self):
        post_title = self.cleaned_data['post_title']
        if '@' in post_title or '-' in post_title or '|' in post_title or '&' in post_title:
           raise forms.ValidationError("Titles should not have special characters.")
        return post_title

    def clean_post_org_name(self):
        post_org_name = self.cleaned_data['post_org_name']
        if '@' in post_org_name or '-' in post_org_name or '|' in post_org_name or '&' in post_org_name:
           raise forms.ValidationError("Name should not have special characters.")
        return post_org_name

    def clean_post_org_address(self):
        post_org_address = self.cleaned_data['post_org_address']
        post_org_address = escape(post_org_address)
        return post_org_address

    def clean_post_org_country(self):
        post_org_country = self.cleaned_data['post_org_country']
        post_org_country = escape(post_org_country)
        return post_org_country

    def clean_post_desc(self):
        post_desc = self.cleaned_data['post_desc']
        post_desc = escape(post_desc)
        return post_desc


class EditProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'accept': 'image/png,.jpg'}))

    class Meta:
        model = Profile
        fields = ['org_name', 'org_role', 'org_email', 'org_phone', 'org_address',
                  'org_city', 'org_state', 'org_zipcode', 'org_country', 'image', 'org_desc']

    def clean_org_name(self):
        org_name = self.cleaned_data['org_name']
        if '@' in org_name or '-' in org_name or '|' in org_name or '&' in org_name:
           raise forms.ValidationError("Name should not have special characters.")
        return org_name

    def clean_org_address(self):
        org_address = self.cleaned_data['org_address']
        org_address = escape(org_address)
        return org_address
        
    def clean_org_country(self):
        org_country = self.cleaned_data['org_country']
        org_country = escape(org_country)
        return org_country

    def clean_org_desc(self):
        org_desc = self.cleaned_data['org_desc']
        org_desc = escape(org_desc)
        return org_desc

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        self.fields['password1'].help_text = 'Password must contain at least 8 characters.'
        self.fields['password2'].help_text = ''
        if 'username' in self.fields:
            print("deleting username from form")
            del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email", "your_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.email = self.cleaned_data.get('email')
        password_validation.validate_password(
            self.cleaned_data.get('password2'), self.instance
        )
        return password2


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        self.fields['password'].help_text = 'Password must contain at least 8 characters'
        self.fields['password'].help_text = ' '
        if 'username' in self.fields:
            print("deleting username from form")
            del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.email = self.cleaned_data.get('email')
        password_validation.validate_password(
            self.cleaned_data.get('password2'), self.instance
        )
        return password2

