from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from main.models import Users
from .models import Membertransaction
from .forms import CheckoutForm
from django.db import DatabaseError
from django.template import loader, Context
import json
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
import datetime

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."
KeyErrorMessage = "Erros when accessing the object"
ExceptionMessage = "Some Exceptions Happened"
AuthorizationError = "Not Authorized"
# Create your views here.

@csrf_exempt
@sensitive_post_parameters()
def profile(request):
    """ This method only deals with one HTTP: GET. 
        When GET, the system will list information
        of the current user, after he loggin. Inlcuding 
        his name and membership status.
    """
    current_user = request.user
    if not current_user.is_authenticated:
            return HttpResponse(AuthorizationError, status = 401)
    else:
        # renders all profile data to the page.
        if request.method == 'GET':
            return render(
                request, 
                '../templates/membership/specificUser.html', 
                {'user': current_user}, 
                status = 200
                )
        else:
            return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
def updateMembership(request):
    """ This method only deals with one HTTP: GET. 
        When GET, the system list out all membership
        types for the user ot choose.
    """
    current_user = request.user
    # check the user's authentification
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        # list out all membership options
        if request.method == 'GET':
            return render(request, '../templates/membership/memberships.html', status = 200)
        else:
            return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
def purchase(request, theType):
    """ This method deals with two HTTP methods: GET 
        and POST. When GET, the server will render a 
        purchase form that allows users to fill all 
        ofourchase data including card number. When
        POST, the system whether the user has fill
        all data in the form appropriately. If so, 
        it creates a new membership transaction obejct 
        and saves it into the database.
    """
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        # renders the checkout form
        if request.method == 'GET':
            form = CheckoutForm()
            return render(
                request, 
                '../templates/membership/purchase.html', 
                {'form': form}, 
                status = 200
                )
        elif request.method == 'POST':
            form = CheckoutForm(request.POST)
            if not form.is_valid():
                return HttpResponse("Invalid registration request.", status = 400)
            else:
                # change the user's membership status to 'member' if he
                # is just a 'normal'. Create a new tranction model.
                the_user = Users.objects.filter(id = request.user.id).get()
                the_user.membership = 'member'
                the_user.save()
                auto_new = form.cleaned_data['auto_renew']
                if theType == 1:
                    if auto_new == 'Yes':
                        total_price = 15
                    else:
                        total_price = 20
                else:
                    if auto_new == 'Yes':
                        total_price = 100
                    else:
                        total_price = 120
                new_transaction = Membertransaction.objects.create(
                        user = request.user,
                        membership = 'member',
                        total_price = total_price
                    ) 
                new_transaction.save()
                return HttpResponseRedirect('/user/transactions')
        else:
            return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
def transactions(request):
    """ It only deals with one HTTP method: GET. When
        GET, it list all membership transaction history.
        The user has to log in to do this.
    """
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        # list out all membership transaction history.
        if request.method == 'GET':
            all_transactions = list(Membertransaction.objects.filter(user = current_user).all().values())
            return render(
                request, 
                '../templates/membership/transactions.html', 
                {'allTransactions': all_transactions, 'user_id': request.user.id},
                status = 200
            )
        else:
            return HttpResponse(BadRequestMessage, status = 405)