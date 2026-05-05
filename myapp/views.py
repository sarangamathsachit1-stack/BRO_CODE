from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'myapp/home.html')

def register(request):
    return render(request, 'myapp/register.html')

def onboarding(request):
    return render(request, 'myapp/onboarding.html')

def login_view(request):
    return render(request, 'myapp/login.html')

def dashboard(request):
    return render(request, 'myapp/dashboard.html')
