from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from main.models import Movies, Users, Reviews, Tickets, Offers
from .models import Cart
from .forms import CartForm, CartDeleteForm
from django.db import DatabaseError
from django.template import loader, Context
import json
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
import datetime
# Create your views here.

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."
KeyErrorMessage = "Erros when accessing the object"
ExceptionMessage = "Some Exceptions Happened"
AuthorizationError = "Not Authorized"

@csrf_exempt
@sensitive_post_parameters()
def jsonHandling(request):
    """ This function's main purpose is to manage error handling for 
    when retrieving and decoding the JSON from the request body. """
    # check if there are errors in the posted data
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JSONDecodeFailMessage
    except Exception:
        return ExceptionMessage
    else:
        return data

@csrf_exempt
@sensitive_post_parameters()
def cart(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        if request.method == 'GET':
            try:
                # get all transactions and return as a list
                cart_list = list(Cart.objects.all().values().filter(user= request.user.id))
                returnList = []
                for cart in cart_list:
                    curCart = {}
                    curCart['id'] = cart.id
                    curCart['ticket'] = cart.ticket.movie.name
                    curCart['quantity'] = cart.quantity
                    curCart['offer'] = cart.offer.name
                    curCart['total_price'] = cart.total_price
                    returnList.append(curCart)
                return render(
                    request, 
                    '../templates/buytickets/cart.html', 
                    {'cartList': cart_list}, 
                    status = 200
                    )
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
        
        elif request.method == 'POST':
            return HttpResponse(ExceptionMessage, status = 400)

        elif request.method == 'PATCH':   
            if not form.is_valid():
                return HttpResponse("Bad login form.", status = 400)
            
            try:
                offer_id = form.cleaned_data['offer_id']

                offerObj = Offers.objects.get(id = offer_id)
                
                if current_user.membership != 'member':
                    cart_list = list(Cart.objects.all().values().filter(user= request.user.id))

                    for cart in cart_list:
                        cartId = cart.id
                        Cart.objects.filter(id = cartId).update(offer = offerObj)
                
                return HttpResponseRedirect('/cart')
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)

        
        elif request.method == 'DELETE':
            form = CartDeleteForm(request.DELETE)
            if not form.is_valid():
                return HttpResponse("Bad login form.", status = 400)
            try:
                del_id = form.cleaned_data['cart_id']
                cart_item = Cart.objects.get(id = del_id)
                ticket_id = cart_item.ticket.id
                ticket_amount = cart_item.ticket.amount
                quant = cart_item.quantity
                
                Cart.objects.filter(id= del_id).delete()
                Tickets.objects.filter(id= ticket_id).update(quantity= ticket_amount + quant)
                
                return HttpResponseRedirect('/cart')
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
        else:
            return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt              
@sensitive_post_parameters()
def checkout(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        if request.method == 'GET':
            form = CartForm()
            return render(request, '../templates/buytickets/purchaseform.html', {'form': form}, status = 200)
        elif request.method == 'POST':
            form = CartForm(request.POST)
            if not form.is_valid():
                return HttpResponse("Invalid registration request.", status = 400)
            else:
                cartList = list(Cart.objects.all().values().filter(user= request.user.id))
                for cart in cartList:
                    
                    the_user = Users.objects.filter(id = cart.user.id).get()
                    the_ticket = Tickets.objects.filter(id = cart.ticket.id).get()
                    the_quantity = cart.quantity
                    the_offer = Offers.objects.filter(id = cart.offer.id).get()
                    the_total_price = cart.total_price
                    
                    new_transaction = Transactions.objects.create(
                        user = the_user, 
                        ticket = the_ticket, 
                        quantity = the_quantity, 
                        offer = the_offer, 
                        total_price = the_total_price
                        )
                    new_transaction.save()
                    Cart.objects.get(id = cart.id).delete()

                return HttpResponseRedirect('/transactions')
        else:
            return HttpResponse(BadRequestMessage, status = 405)