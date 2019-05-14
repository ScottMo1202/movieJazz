from django.shortcuts import render
from django.http import HttpResponse
from .forms import ReigistrationForm, SigninForm 
from django.http import HttpResponseRedirect 
from django.contrib.auth import authenticate, login, logout
from main.models import Users
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
from django.db import DatabaseError
import json


JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."
KeyErrorMessage = "Erros when accessing the object"
ExceptionMessage = "Some Exceptions Happened"
AuthorizationError = "Not Authorized"

# Create your views here.

def adminUser():
    """ This will create an admin user, which is specifically for internal use.
    The user will only be created if it does not exist already. """

    # Checking if general channel exists
    if len(Users.objects.all().values().filter(membership="administrator", username="admin")) == 0:
        
        # Try to create admin user if it does not already exist
        try:
            user = Users.objects.create_user(username = "admin", password = "admin", first_name = "Admin")
            user.membership="administrator"
            user.last_name = 'Account'
            user.email = 'admin@email.com'
            user.save()
        
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)

adminUser()

@csrf_exempt
@sensitive_post_parameters()
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
            user = Users.objects.create_user(username = username, password = password, first_name = first_name)
            user.last_name = last_name
            user.email = email
            user.save()

            return HttpResponseRedirect('/auth/signin')
    else:
        return HttpResponse("Method not allowed", status = 405)

@csrf_exempt
@sensitive_post_parameters()
def signin(request):
    if request.method == 'GET':
        form = SigninForm()
        return render(request, '../templates/auth/signin.html', {'form': form}, status = 200)
    elif request.method == 'POST':
        form = SigninForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Bad login form.", status = 400)
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Invalid credentials.", status = 401)
    else:
        return HttpResponse("Method not allowed on /auth/signin.", status = 405)

@csrf_exempt
@sensitive_post_parameters()
def signout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('Sign out successful.', status = 200)
        else:
            return HttpResponse('Not logged in.', status = 200)
    else:
        return HttpResponse("Method not allowed on /auth/signout.", status = 405)

