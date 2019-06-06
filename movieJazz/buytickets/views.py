from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from main.models import Movies, Users, Reviews, Tickets, Offers, Transactions
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
    """ This functions deals with only the GET method. 
        The user has to login to call it. It will get
        all items(movie tickets) in the shopping cart and renders as a 
        list to the html template.
    """
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        if request.method == 'GET':
            try:
                # get all cart items of the user, including the ticket name,
                # time, quantity, offer, and total_price after applying the 
                # offer.
                cart_list = list(Cart.objects.all().filter(user= request.user.id))
                returnList = []
                for cart in cart_list:
                    curCart = {}
                    curCart['id'] = cart.id
                    curCart['ticket'] = cart.ticket.movie.name
                    curCart['time'] = cart.ticket.time
                    curCart['quantity'] = cart.quantity
                    curCart['offer'] = cart.offer.offer_name
                    curCart['total_price'] = float(cart.total_price)
                    returnList.append(curCart)
                
                return render(
                    request, 
                    '../templates/buytickets/cart.html', 
                    {'cartList': returnList}, 
                    status = 200
                    )
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
def addOffer(request, off_id):
    """This method onoly deals with one HTTP method: GET.
       When GET, the system if the user has a status of member.
       If so, it could apply to all the items to the buy and calculate
       a discounted price. 
    """
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        if request.method == 'GET':   
            try:
                offerObj = Offers.objects.get(id = off_id)
                # check whether the user is a member, if so, apply 
                # appropriate offers to him.
                if current_user.membership != 'member':
                    cart_list = list(Cart.objects.all().filter(user= request.user.id))

                    for cart in cart_list:
                        the_total_price = float(cart.quantity) * float(
                            cart.ticket.price) * float(1 - offerObj.offer_perc)
                        the_total_price = round(the_total_price, 2)
                        Cart.objects.filter(id = cart.id).update(
                            offer = offerObj, 
                            total_price = the_total_price
                            )
                
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
def alterCart(request, cart_id):
    """This method with deals with one HTTP methos: GET
       When GET, the system will delete things from the cart
       but will it will add back the number, refering to how 
       many items they user wanted to buy, to the stock. For example,
       if there are 57 tickets left, and the user added three into the cart.
       If the user decides not to buy it and delte the cart, the 
       three tickets will be added back to the stock, which means that
       now the stock has 60 tickets left.
    """
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:     
        if request.method == 'GET':
            # 
            try:
                # add the deleted amount back to the model.
                del_id = cart_id
                cart_item = Cart.objects.get(id = del_id)
                ticket_id = cart_item.ticket.id
                ticket_amount = cart_item.ticket.amount
                quant = cart_item.quantity
                Cart.objects.filter(id= del_id).delete()
                Tickets.objects.filter(id= ticket_id).update(amount= ticket_amount + quant)
                
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
    """This function deals with two Http method, one is GET, which renders
       a checkout form where the user needs to fill his data including 
       card information. The POST method will check whether fill all
       valid data and create a new tickets transaction model and save it into
       the database.
    """
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        # renders the purchase form
        if request.method == 'GET':
            form = CartForm()
            return render(
                request, 
                '../templates/buytickets/purchaseform.html', 
                {'form': form}, 
                status = 200
                )
        elif request.method == 'POST':
            form = CartForm(request.POST)
            if not form.is_valid():
                return HttpResponse("Invalid registration request.", status = 400)
            else:
                cartList = list(Cart.objects.all().filter(user= request.user.id))
                for cart in cartList:
                    # create a new transaction history and save it into the database
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