from django.shortcuts import render
from django.http import HttpResponse
from .models import InfoPrompt
# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"InfoPrompt": InfoPrompt.objects.all})
def contact(request):
    return render(request=request,
                  template_name="main/contact.html")#,
                 # context={"InfoPrompt": InfoPrompt.objects.all})

def login(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def signup(request):
    return render(request=request,
                  template_name="main/signup.html")