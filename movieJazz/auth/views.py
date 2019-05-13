from django.shortcuts import render
from django.http import HttpResponse
from .forms import ReigistrationForm, SigninForm 
from django.http import HttpResponseRedirect 
from django.contrib.auth import authenticate, login, logout
from main.models import Users
from django.views.decorators.debug import sensitive_post_parameters
# Create your views here.

@sensitive_post_parameters('password', 'passwordconf', 'username', 'email', 
                           'first_name', 'last_name')
def register(request):
    if request.method == 'GET':
        form = ReigistrationForm()
        return render(request, '../templates/auth/register.html', {'form': form}, status = 200)
    elif request.method == 'POST':
        form = ReigistrationForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Invalid registration request.", status = 400)
        else:
            password = form.cleaned_data['password']
            passwordconf = form.cleaned_data['passwordconf']
            if not password == passwordconf:
                return HttpResponse("Passwords did not match.", status = 400)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = Users.objects.create(username = username, password = password, first_name = first_name)
            user.last_name = last_name
            user.email = email
            user.save()

            return HttpResponseRedirect('/auth/signin')
    else:
        return HttpResponse("Method not allowed", status = 405)

@sensitive_post_parameters('username', 'password')
def signin(request):
    if request.method == 'GET':
        form = SigninForm()
        return render(request, '../templates/auth/signin.html', {'form': form}, status = 200)
    elif request.method == 'POST':
        form = SigninForm(request.POST)
        if not form.is_valid:
            return HttpResponse("Bad login form.", status = 400)
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Invalid credentials.", status = 401)
    else:
        return HttpResponse("Method not allowed on /auth/signin.", status = 405)

def signout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('Sign out successful.', status = 200)
        else:
            return HttpResponse('Not logged in.', status = 200)
    else:
        return HttpResponse("Method not allowed on /auth/signout.", status = 405)

