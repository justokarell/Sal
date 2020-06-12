# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


# class NewUserForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")

#     def save(self, commit=True):
#         user = super(NewUserForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user

# class NewUserForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     orgname = forms.CharField(required=True)
#     phone = forms.CharField(required=True)
#     address = forms.CharField(required=True)

#     class Meta:
#         model = User
#         fields = ("username", "orgname", "email", "phone", "address",  "password1", "password2")

#     def save(self, commit=True):
#         user = super(NewUserForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         user.orgname = self.cleaned_data["orgname"]
#         user.phone = self.cleaned_data["phone"]
#         user.address = self.cleaned_data["address"]
#         if commit:
#             user.save()
#         return user

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from appname.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser