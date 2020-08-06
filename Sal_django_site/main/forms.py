import os
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
# from address.forms import AddressField, AddressWidget
from django.forms import ModelForm

class EditProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class ProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'accept':'image/png,.jpg'}))

    class Meta:
        model = Profile
        fields = ['org_name', 'org_role','org_email','org_phone','org_address','org_city','org_state','org_zipcode','org_country','image','org_desc']
    
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
    
# class PersonForm(forms.Form):
#     address = AddressField()