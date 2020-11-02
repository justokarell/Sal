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
from .tokens import user_tokenizer
from rest_framework import serializers
from .models import InfoPrompt, CustomUser, Profile, UserPost, DonorPost, RecipientPost, Availability
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
import json
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactForm
from .serializers import UserPostSerializer, AvailabilitySerializer
from django.core.serializers.json import DjangoJSONEncoder
from address.models import Address
from .forms import ProfileForm, EditProfileForm, DonorPostForm, RecipientPostForm, AvailabilityFormset
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"InfoPrompt": InfoPrompt.objects.all})

def volunteerView(request):
    return render(request=request,
                  template_name="main/volunteer.html")
    
def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                # send_mail(subject, message, from_email, ['salhateswaste@gmail.com'])
                mail = EmailMessage(subject, message, to=['salhateswaste@gmail.com'], from_email=from_email)
                mail.content_subtype = 'html'
                mail.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request=request, template_name="main/email.html", context={'form': form})

def successView(request):
    return render(request=request, template_name="main/success.html")
    # return HttpResponse('Success! Thank you for your message.')


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
            Profile.objects.create(user=user)
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

            return redirect("homepage")

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
    return redirect("homepage")


class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id).decode())
        
        user = CustomUser.objects.get(pk=user_id)

        context = {
          'form': AuthenticationForm(),
          'message': 'Registration confirmation error . Please click reset password to generate a new confirmation email.'
        }
        if user and user_tokenizer.check_token(user, token):
            user.is_valid = True
            user.save()
            context['message'] = 'Registration complete. Please login'

        messages.success(request, f"Your account has been registered")
        return redirect('login')

def account_activation_sent(request):
    return render(request=request,
                  template_name="main/account_activation_sent.html")#,
                 # context={"InfoPrompt": InfoPrompt.objects.all})

def reset_password(request):
    return render(request=request,
                  template_name="main/reset_password.html")#,

def reset_confirmation_sent(request):
    return render(request=request,
                  template_name="main/reset_confirmation_sent.html")#,
                 # context={"InfoPrompt": InfoPrompt.objects.all})
                 
def map_page(request):
    # top = request.GET['top']
    # bottom = request.GET['bottom']
    # right = request.GET['right']
    # left = request.GET['left']
#I have examples set up so we can either return a json or a list of post objects whatever's easier


    # post_list = Post.objects.\
    #     filter(latitude__gte=bottom).\
    #     filter(latitude__lte=top). \
    #     filter(longitude__gte=left).\
    #     filter(longitude__lte=right)

    # if int(request.GET['zoom']) > 13 or len(post_list) < 2000:
    #     result = serialize('json', post_list,
    #                fields=('uid', 'latitude', 'longitude'))
    # return HttpResponse(result)

    # post_list = UserPost.objects.all().values()
    


    post_list = UserPost.objects.all()
    serializer = UserPostSerializer(post_list, many=True)
    result = json.dumps(serializer.data)

    return render(request=request, template_name="main/map_page.html", context={"result":result})
                  

def profile_view(request):
    if request.user.is_authenticated:
        return render(request=request,template_name="main/profile_view.html")
    else:
        messages.info(request, f"Login to view your profile")
        return redirect('login')

@login_required
def profile_edit(request):
 if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  # request.FILES is show the selected image or file
    
        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            messages.success(request, f"Your profile has been updated")
            return redirect('profile-view')
        else:
            for msg in profile_form.errors:
                messages.error(request, f"Some of your input is off. Try again.")

            return render(request = request,
                          template_name = "main/profile_edit.html",
                          context={"form":form, "profile_form":profile_form})
 else:
    form = EditProfileForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'main/profile_edit.html', context = {'form': form,
               'profile_form': profile_form})

def delete(request, single_slug = None):
    instance = get_object_or_404(UserPost, post_slug = single_slug)
    instance.delete()
    return redirect('my-posts')
    return render(request=request, template_name="main/my_posts.html")

def edit_rpost(request, single_slug = None):
    user = request.user
    instance = get_object_or_404(RecipientPost, post_slug = single_slug)
    avail_instance = AvailabilityFormset(queryset=Availability.objects.all())
    if request.method == "POST":
        recipient_post_form = RecipientPostForm(request.POST or None, request.FILES or None, instance=instance or None)
        avail_form = AvailabilityFormset(request.POST, request.FILES, instance=instance)

        if recipient_post_form.is_valid():
            
            recipient_post = recipient_post_form.save()
            coord = recipient_post.get_geocode()
            recipient_post.post_lat = coord[0]
            recipient_post.post_long = coord[1]
            recipient_post.save() 
            recipient_post.save() 
            if avail_form.is_valid():
                availslist = avail_form.save()
                for avail in availslist:
                    # avail.assigned_post = recipient_post
                    time = avail.get_min()
                    avail.start_min = time[0]
                    avail.end_min = time[1]
                    avail.save()
                recipient_post.save()
                messages.success(request, f"Your post has been updated")
                return redirect('my-posts')  
            else:
                messages.error(request, f"Your availability input is off. Try again.")
                # for errors in avail_form.errors:
                #     messages.error(request, f"Your availability is off. Try again.")
            
        
        else: 
            for errors in recipient_post_form.errors:
                    messages.error(request, f"Some of your input is off. Try again.")
    else:
        recipient_post_form = RecipientPostForm(instance=instance)
        avail_form = AvailabilityFormset(instance=instance)

    return render(request=request, template_name="main/edit_rpost.html", context = {
                                                                "instance": instance,
                                                                "avail_form": avail_form,
                                                                "recipient_post_form": recipient_post_form})

def new_rpost(request):
    user = request.user
    profile = request.user.profile
    
    if request.method == "POST":
        recipient_post_form = RecipientPostForm(request.POST, request.FILES)
        avail_form = AvailabilityFormset(request.POST, request.FILES)

        if recipient_post_form.is_valid():
            
            recipient_post = recipient_post_form.save(False)
            recipient_post.post_creator = user
            recipient_post.donor_or_recip = "Recipient"
            coord = recipient_post.get_geocode()
            recipient_post.post_lat = coord[0]
            recipient_post.post_long = coord[1]
            recipient_post.save() 
            if avail_form.is_valid():
                availslist = avail_form.save(False)
                for avail in availslist:
                    avail.assigned_post = recipient_post
                    time = avail.get_min()
                    avail.start_min = time[0]
                    avail.end_min = time[1]
                    avail.save()
                recipient_post.save()
                messages.success(request, f"Your post has been uploaded")
                return redirect('my-posts')  
            else:
                for errors in avail_form.errors:
                    messages.error(request, f"Your availability is off. Try again.")
            
        
        else: 
            for errors in recipient_post_form.errors:
                    messages.error(request, f"Some of your input is off. Try again.")
    else:
        recipient_post_form = RecipientPostForm(initial={'post_org_name': profile.org_name, 'post_org_email':profile.org_email,
        'post_org_phone':profile.org_phone,'post_org_address':profile.org_address,'post_org_city':profile.org_city,
        'post_org_state':profile.org_state,'post_org_zipcode':profile.org_zipcode,'post_org_country':profile.org_country})
        avail_form = AvailabilityFormset()

    
    return render(request=request, template_name="main/new_rpost.html", context = {
                                                               "profile" : profile,
                                                                "avail_form": avail_form,
                                                                "recipient_post_form": recipient_post_form})
def edit_dpost(request, single_slug = None):
    user = request.user
    instance = get_object_or_404(DonorPost, post_slug = single_slug)
    avail_instance = AvailabilityFormset(queryset=Availability.objects.all())
    if request.method == "POST":
        donor_post_form = DonorPostForm(request.POST or None, request.FILES or None, instance=instance or None)
        avail_form = AvailabilityFormset(request.POST, request.FILES, instance=instance)

        if donor_post_form.is_valid():
            
            # donor_post = donor_post_form.save(False)
            donor_post = donor_post_form.save()
            coord = donor_post.get_geocode()
            donor_post.post_lat = coord[0]
            donor_post.post_long = coord[1]
            donor_post.save()
            if avail_form.is_valid():
                availslist = avail_form.save()
                for avail in availslist:
                    time = avail.get_min()
                    avail.start_min = time[0]
                    avail.end_min = time[1]
                    avail.save()
                donor_post.save()
                messages.success(request, f"Your post has been updated")
                return redirect('my-posts')  
            else:
                messages.error(request, f"Your availability input is off. Try again.")
                # for errors in avail_form.errors:
                #     messages.error(request, f"Your availability is off. Try again.")

        else: 
            for errors in donor_post_form.errors:
                    messages.error(request, f"Some of your input is off. Try again.")
    else:
        donor_post_form = DonorPostForm(instance=instance)
        avail_form = AvailabilityFormset(instance=instance)

    return render(request=request, template_name="main/edit_dpost.html", context = {
                                                                "instance": instance,
                                                                "avail_form": avail_form,
                                                                "donor_post_form": donor_post_form})

def new_dpost(request):
    user = request.user
    profile = request.user.profile
    

    if request.method == "POST":
        donor_post_form = DonorPostForm(request.POST, request.FILES)
        avail_form = AvailabilityFormset(request.POST, request.FILES)

        if donor_post_form.is_valid():
            
            donor_post = donor_post_form.save(False)
            donor_post.post_creator = user
            donor_post.donor_or_recip = "Donor"
            coord = donor_post.get_geocode()
            donor_post.post_lat = coord[0]
            donor_post.post_long = coord[1]
            donor_post.save() 
            if avail_form.is_valid():
                availslist = avail_form.save(False)
                for avail in availslist:
                    avail.assigned_post = donor_post
                    time = avail.get_min()
                    avail.start_min = time[0]
                    avail.end_min = time[1]
                    avail.save()
                donor_post.save()
                messages.success(request, f"Your post has been uploaded")
                return redirect('my-posts')  
            else:
                for errors in avail_form.errors:
                    messages.error(request, f"Your availability is off. Try again.")
            
        
        else: 
            for errors in donor_post_form.errors:
                    messages.error(request, f"Some of your input is off. Try again.")
    else:
        donor_post_form = DonorPostForm(initial={'post_org_name': profile.org_name, 'post_org_email':profile.org_email,
        'post_org_phone':profile.org_phone,'post_org_address':profile.org_address,'post_org_city':profile.org_city,
        'post_org_state':profile.org_state,'post_org_zipcode':profile.org_zipcode,'post_org_country':profile.org_country})
        avail_form = AvailabilityFormset()

    
    return render(request=request, template_name="main/new_dpost.html", context = {
                                                               "profile" : profile,
                                                                "avail_form": avail_form,
                                                                "donor_post_form": donor_post_form})

def my_account(request):
    user = request.user
    return render(request=request, template_name="main/my_account.html", context={'user': user})

def my_posts(request):
    if request.user.is_authenticated:
        user = request.user
        my_posts = UserPost.objects.filter(post_creator = user)
        return render(request=request, template_name="main/my_posts.html", context = {
                                                               "my_posts" : my_posts})
    else:
        messages.info(request, f"Login to view your posts")
        return HttpResponseRedirect('login')
    return render(request=request, template_name="main/my_posts.html")

def single_slug(request, single_slug):

    posts = [p.post_slug for p in UserPost.objects.all()]
    if single_slug in posts:
        matching_post = UserPost.objects.filter(post_slug=single_slug).first()
        return render(request=request,
                      template_name='main/single_post.html',
                      context={"single_post": matching_post})
    
    profiles = [r.profile_slug for r in Profile.objects.all()]
    if single_slug in profiles:
        matching_profile = Profile.objects.filter(profile_slug=single_slug).first()
        this_org = matching_profile.user
        return render(request=request,
                      template_name='main/other_profiles.html',
                      context={"this_org":this_org})

    return HttpResponse(f"'{single_slug}' does not correspond to anything we know of!") 