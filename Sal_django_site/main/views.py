from django.shortcuts import render, redirect 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
# from .tokens import account_activation_token
from .tokens import user_tokenizer
from .models import InfoPrompt, CustomUser
#new stuff
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"InfoPrompt": InfoPrompt.objects.all})
def contact(request):
    return render(request=request,
                  template_name="main/contact.html")#,
                 # context={"InfoPrompt": InfoPrompt.objects.all})
def email_test1(request):
    return render(request=request,
                  template_name="main/account_activation_email.html")
def email_test2(request):
    return render(request=request,
                  template_name="main/reset_password_email.html")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        # form = UserCreationForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            token = user_tokenizer.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'user_id': user_id, 'token': token})
            message = get_template("main/account_activation_email.html").render({
              'confirm_url': url
            })
            mail = EmailMessage('Sal Hates Waste Confirmation Email', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
            mail.content_subtype = 'html'
            mail.send()
            messages.success(request,  f'A confirmation email has been sent to {user.email}. Please confirm to finish registering')

            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"Some of your input is off. Try again.")

            return render(request = request,
                          template_name = "main/signup.html",
                          context={"form":form})

    form = CustomUserCreationForm()
    # form = UserCreationForm()
    return render(request = request,
                  template_name = "main/signup.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id).decode())
        
        user = CustomUser.objects.get(pk=user_id)

        context = {
          'form': AuthenticationForm(),
          'message': 'Registration confirmation error . Please click the reset password to generate a new confirmation email.'
        }
        if user and user_tokenizer.check_token(user, token):
            user.is_valid = True
            user.save()
            context['message'] = 'Registration complete. Please login'

        messages.success(request, f"You're accoount has been registered")
        return redirect('main:login')

def account_activation_sent(request):
    return render(request=request,
                  template_name="main/account_activation_sent.html")#,
                 # context={"InfoPrompt": InfoPrompt.objects.all})

def reset_confirmation_sent(request):
    return render(request=request,
                  template_name="main/reset_confirmation_sent.html")#,
                 # context={"InfoPrompt": InfoPrompt.objects.all})