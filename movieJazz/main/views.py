from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Theaters, Transactions, Tickets, Movies, Users, Offers
from django.db import DatabaseError
import json
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
import datetime
from buytickets.models import Cart
from .forms import AddCartForm
# Create your views here.

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."
KeyErrorMessage = "Erros when accessing the object"
ExceptionMessage = "Some Exceptions Happened"
AuthorizationError = "Not Authorized"


def defaultOffer():
    """ This will create an offer with 0% off, which is specifically for no offer used.
    The offer will only be created if it does not exist already. """

    # Checking if 'No Offer' exists
    if len(Offers.objects.all().values().filter(
        offer_name="No Offer", offer_perc=.00, description = "No Offer")) == 0:
        
        # Try to create default offer if it does not already exist
        try:
            offer = Offers.objects.create(
                offer_name = "No Offer", 
                offer_perc =.00 , 
                description = "No Offer"
                )
            offer.save()
        
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
    
    if len(Offers.objects.all().values().filter(
        offer_name="Membership", offer_perc=.40, description = "Membership")) == 0:
        
        # Try to create default offer if it does not already exist
        try:
            offer = Offers.objects.create(
                offer_name = "Membership", 
                offer_perc =.40 , 
                description = "Membership"
                )
            offer.save()
        
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)

@csrf_exempt
@sensitive_post_parameters()
def home(request):
    """ This view handles rending the main page of the website with the all the 
    links to different areas of the page such as signin/signout, movies,
    offers, etc. """
    # go to the home page
    if request.method == 'GET':
        return render(request, '../templates/main/index.html', status = 200)
    else:
        return HttpResponse("Method not allowed on /.", status = 405)

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
def theaters(request):
    """ This view handles all requests made to /theaters route. When a
    GET request is made, all the theaters currently within the website
    database will be displayed, including their information about address.
    When a POST request is made (only admins can add theaters to website)
    new Theaters can be added to database, by specifying name and address 
    info."""
    if request.method == 'GET':
        try:
            theater_list = list(Theaters.objects.all().values())
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return all theaters into the template
            return render(
                request, 
                '../templates/main/theaters.html', 
                {'theaters': theater_list},
                status = 200
                )
    elif request.method == 'POST':
        # if the user is logged in
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        current_user = request.user
        # check if the user has right authorization
        if current_user.membership != 'administrator' and current_user.membership != 'seller':
            return HttpResponse(AuthorizationError, status = 401)
        else:
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                try:
                    # create a new theater
                    new_theater = Theaters.objects.create(
                        name = posted_data['name'], 
                        street_number = posted_data['street_number'], 
                        street_name = posted_data['street_name'], 
                        city = posted_data['city'], 
                        state = posted_data['state'], 
                        post_code = posted_data['post_code']
                        )
                    new_theater.save()
                    new_theater_info = Theaters.objects.all().values().filter(pk = new_theater.pk)[0]
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status = 400)
                except KeyError:
                    return HttpResponse(KeyErrorMessage, status = 400)
                except Exception:
                    return HttpResponse(ExceptionMessage, status = 400)
                else:
                    # return the newly created theater as a json object
                    return JsonResponse(
                        new_theater_info, 
                        safe = False, 
                        content_type = 'application/json', 
                        status = 201
                        )
    else:
        return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
@sensitive_post_parameters()
def specificTheater(request, theater_id):
    """ This view handles all requests made to /theaters/<id>. When a GET
    request is made, all the information specific to the theater is displayed.
    When a PATCH request is made (only admins can patch and delete) information
    about the theater such as name and address can be changed and saved. When 
    a DELETE request is made, the specific theater will be deleted from the
    website."""
    if request.method == 'GET':
        try: 
            # filter the specified theater
            the_theater = Theaters.objects.filter(id = theater_id).get()
            the_theater_data = {
                "name": the_theater.name, 
                'street_number': the_theater.street_number, 
                'street_name': the_theater.street_name, 
                'city': the_theater.city, 
                'state': the_theater.state, 
                'post_code': the_theater.post_code
                }
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return the theater data as a json object
            return JsonResponse(
                the_theater_data, 
                safe = False, 
                content_type = 'application/json', 
                status = 201
                )
    elif request.method == 'PATCH':
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        current_user = request.user
        if current_user.membership != 'administrator' and current_user.membership.name != 'seller':
            return HttpResponse(AuthorizationError, status = 403)
        else:
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                try:
                    the_theater = Theaters.objects.filter(id = theater_id).get()
                    changed_data = {}
                    # checks what types of data the user wants to modify for the 
                    # theater
                    if 'name' in posted_data:
                        the_theater.name = posted_data['name']
                        changed_data['name'] = posted_data['name']
                    if 'street_number' in posted_data:
                        the_theater.street_number = posted_data['street_number']
                        changed_data['street_number'] = posted_data['street_number']
                    if 'street_name' in posted_data:
                        the_theater.street_name = posted_data['street_name']
                        changed_data['street_name'] = posted_data['street_name']
                    if 'city' in posted_data:
                        the_theater.city = posted_data['city']
                        changed_data['city'] = posted_data['city']
                    if 'post_code' in posted_data:
                        the_theater.post_code = posted_data['post_code']
                        changed_data['post_code'] = posted_data['post_code']
                    the_theater.save()
                except KeyError:
                    return HttpResponse(KeyErrorMessage, status = 400)
                except DatabaseError:
                    return HttpResponse(DatabaseError, status = 400)
                except Exception:
                    return HttpResponse(ExceptionMessage, status = 400)
                else:
                    # return the modified data as a json object
                    return JsonResponse(
                        changed_data, 
                        safe = False, 
                        content_type = 'application/json', 
                        status = 201
                        )
    # delete the specified theater
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        if request.user.membership != 'administrator' and request.user.membership.name != 'seller':
            return HttpResponse(AuthorizationError, status = 403)
        try:
            Theaters.objects.filter(id= theater_id).delete()
        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return a plain text message if the theater is deleted
            # successfully
            return HttpResponse('Deleted', status = 200)
    else:
        return HttpResponse(BadRequestMessage, status = 405)




@csrf_exempt
@sensitive_post_parameters()
def tickets(request, theater_id, movie_id):
    """ This view handles all requests made to /theaters/<id>/tickets.
    When a GET request is made, all tickets available in the specific 
    theater will be displayed. When a POST (only admins can post and delete)
    request is made, new tickets can be added to the theater when infomation
    of about movie, price movie type, and time are provided. When a DELETE 
    request is made specific tickets can be deleted from the theater. Only
    tickets for the specified theater can be deleted.
    """
    current_user = request.user
    if request.method == "GET":
        try:
            # get all tickets
            all_tickets = Tickets.objects.filter(theater = theater_id, movie = movie_id).all()
        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return all tickets data as a json object
            return render(
                request,
                '../templates/main/tickets.html',
                {'ticketList': all_tickets},
                status = 200
            )
    
    elif request.method == 'POST':
        if not current_user.is_authenticated:
            return HttpResponse(AuthorizationError, status = 401)
        # checks the user's authorization
        if current_user.membership == 'administrator':
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
                # try to create a new ticket
            try:
                the_ticket_movie = Movies.objects.filter(id = movie_id).get()
                the_ticket_theater = Theaters.objects.filter(id = theater_id).get()
                the_ticket_time = posted_data['time']
                the_ticket_price = posted_data['price']
                the_ticket_movie_type = posted_data['movie_type']
                the_ticket_amount = posted_data['amount']
                new_ticket = Tickets.objects.create(
                    movie = the_ticket_movie, 
                    time = the_ticket_time, 
                    theater = the_ticket_theater, 
                    price = the_ticket_price, 
                    movie_type = the_ticket_movie_type,
                    amount = the_ticket_amount
                    )
                new_ticket.save()
                ticketInfo = Tickets.objects.all().values().filter(pk = new_ticket.pk)[0]
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
            else:
                # return the new ticket data as a json object if created successfully
                return JsonResponse(
                    ticketInfo, 
                    safe = False, 
                    content_type = 'application/json', 
                    status = 201
                    )
        else:
            return HttpResponse(AuthorizationError, status = 403)
    
    elif request.method == 'DELETE':
        if not current_user.is_authenticated:
            return HttpResponse(AuthorizationError, status = 401)
        if current_user.membership == 'administrator':
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            try:
                # check if the ticket is available
                toBeDeleted = Tickets.objects.filter(id = posted_data['id'], theater= theater_id)
                if toBeDeleted is None:
                    return HttpResponse('Ticket not available in Theater.', status = 200)
                toBeDeleted.delete()
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
            else:
                return HttpResponse('Ticket Deleted', status = 200)
        else:
            return HttpResponse(AuthorizationError, status = 403)
    else:
        return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
@sensitive_post_parameters()
def transactions(request):
    """ This view handles all requests made to /transactions. When a GET request is made
    (user need to be logged in and authenticated in order to access any methods)
    the specific user's transactions will display. When a POST request is made, 
    a new transaction is added to the database, with movie, quantity, user, and offer
    info are specified (only admins can make post, patch, and delete requests).
    When a PATCH request is made, specific transaction entries can be updated, by either
    changing quantity, or adding an offer. When a DELETE request is made, specificied
    transactions can be deleted."""
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        if request.method == 'GET':
            try:
                # get all transactions and return as a list
                transaction_list = list(Transactions.objects.all().filter(user= request.user.id))
                returnList = []
                for tran in transaction_list:
                    curTran = {}
                    curTran['movie'] = tran.ticket.movie.name
                    curTran['price'] = tran.ticket.price
                    curTran['time'] = tran.ticket.time
                    curTran['quantity'] = tran.quantity
                    curTran['offer'] = tran.offer.offer_perc
                    curTran['total_price'] = tran.total_price
                    curTran['date'] = tran.date
                    returnList.append(curTran)
                    # return as a json object
                return render(request, '../templates/membership/tickettransactions.html', {'tranList': returnList}, status = 200)
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
                
        
        elif request.method == 'POST':
            # check the user membership
            if current_user.membership == 'administrator':
                posted_data = jsonHandling(request)
                if posted_data == JSONDecodeFailMessage:
                    return HttpResponse(JSONDecodeFailMessage, status = 400)
                try:
                    # try to create a new transaction
                    the_user = Users.objects.filter(id = posted_data['user']).get()
                    the_ticket = Tickets.objects.filter(id = posted_data['ticket']).get()
                    the_quantity = posted_data['quantity']
                    offer = Offers.objects.filter(id = posted_data['offer']).get()
                    the_total_price = float(the_quantity) * float(the_ticket.price) * float(
                        1 - offer.offer_perc)
                    
                    the_total_price = round(the_total_price, 2)
                    new_transaction = Transactions.objects.create(
                        user = the_user, 
                        ticket = the_ticket, 
                        quantity = the_quantity, 
                        offer = offer, 
                        total_price = the_total_price
                        )
                    new_transaction.save()
                    transaction_info = Transactions.objects.all().values().filter(
                        pk = new_transaction.pk
                        )[0]
                    
                except DatabaseError:
                    return HttpResponse(DatabaseError, status = 400)
                except KeyError:
                    return HttpResponse(DatabaseError, status = 400)
                except Exception:
                    return HttpResponse(ExceptionMessage, status = 400)
                else:
                    # return the newly created transaction as a json object
                    return JsonResponse(
                        transaction_info, 
                        safe = False, 
                        content_type = 'application/json', 
                        status = 201
                        )
            else:
                return HttpResponse(AuthorizationError, status = 403)
        
        elif request.method == 'PATCH':
            if current_user.membership == 'administrator':
                posted_data = jsonHandling(request)
                if posted_data == JSONDecodeFailMessage:
                    return HttpResponse(JSONDecodeFailMessage, status = 400)
                try:
                    if 'id' in posted_data:
                        # try to check what information the user wants to modify
                        curTran = Transactions.objects.filter(id=posted_data['id'])
                        if 'quantity' in posted_data:
                            curTran.update(quantity= posted_data['quantity'])
                        if 'offer' in posted_data:
                            newDisc = Offers.objects.get(id=posted_data['offer'])
                            curTran.update(offer= newDisc)
                        
                        the_total_price = float(curTran.get().quantity) * float(
                            curTran.get().ticket.price) * float(1 - curTran.get().offer.offer_perc)

                        the_total_price = round(the_total_price, 2)
                        curTran.update(total_price= the_total_price)

                        tranInfo = Transactions.objects.all().values().filter(id= posted_data['id'])[0]
                        return JsonResponse(
                            tranInfo, 
                            safe = False, 
                            content_type = 'application/json', 
                            status = 201
                            )
                    else:
                        return HttpResponse(BadRequestMessage, status = 405)
                except DatabaseError:
                    return HttpResponse(DatabaseError, status = 400)
                except KeyError:
                    return HttpResponse(KeyErrorMessage, status = 400)
                except Exception:
                    return HttpResponse(ExceptionMessage, status = 400)
            else:
                return HttpResponse(AuthorizationError, status = 403)
        
        elif request.method == 'DELETE':
            if current_user.membership == 'administrator':
                posted_data = jsonHandling(request)
                if posted_data == JSONDecodeFailMessage:
                    return HttpResponse(JSONDecodeFailMessage, status = 400)
                try:
                    #catch and delte the specified transaction
                    Transactions.objects.filter(id = posted_data['id']).delete()
                except DatabaseError:
                    return HttpResponse(DatabaseError, status = 400)
                except KeyError:
                    return HttpResponse(KeyErrorMessage, status = 400)
                except Exception:
                    return HttpResponse(ExceptionMessage, status = 400)
                else:
                    return HttpResponse('Transaction Deleted', status = 200)
            else:
                return HttpResponse(AuthorizationError, status = 403)    
        else:
            return HttpResponse(BadRequestMessage, status = 405)
              
@csrf_exempt
@sensitive_post_parameters()
def users(request):
    """ This view handles all requests made to /users route. Only admin
    can access requests to this route in order to access all user information.
    When a GET request is made, all users and their information are displayed. """
    if request.user.is_authenticated:
        try:
            # check to see if user is admin or not
            if len(Users.objects.all().values().filter(
                id= request.user.id, 
                membership = "administrator"
                )) == 0:
                return HttpResponse("Unauthorized", status=403)
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        
        if request.method == 'GET':
            try:
                # gets a list of all current users
                userList = list(Users.objects.all().values()) 
                return render(
                    # displays list as on formated template
                    request, 
                    '../templates/main/users.html', 
                    {'userList': userList}, 
                    status = 200
                    )
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
        else :
            return HttpResponse("Method not allowed on /users.", status = 405)
    else:
        return HttpResponse(AuthorizationError, status=401)

@csrf_exempt
@sensitive_post_parameters()
def offers(request):
    """ This view handles all requests made to /offers route. When a 
    GET request is made, all offers that are active on the website
    are displayed, including information like name and description.
    When a POST request is made (only admins can post new offers)
    new offers can be added to the website, by specifying name, 
    discount, and description."""
    if request.method == 'GET':
        try:
            # Getting list of all offers
            offersList = list(Offers.objects.all().values()) 

            # Displaying list as formatted template
            return render(
                request, 
                '../templates/main/offers.html', 
                {'offersList': offersList}, 
                status = 200
                )
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
    
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if len(Users.objects.all().values().filter(
                id= request.user.id, 
                membership = "administrator"
                )) == 0:
                return HttpResponse("Unauthorized", status=403)
            
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                try:
                    # Adding and saving new offer into Offers table
                    newOffer = Offers.objects.create(
                        offer_name = posted_data['offer_name'], 
                        offer_perc = posted_data['offer_perc'], 
                        description = posted_data['description']
                        )
                    newOffer.save()
                    offerInfo = Offers.objects.all().values().filter(pk=newOffer.pk)[0]
                    # returns information of recently added offer
                    return JsonResponse(
                        offerInfo, 
                        safe = False, 
                        content_type = 'application/json', 
                        status = 201
                        )
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status=400)
                except KeyError:
                    return HttpResponse(KeyErrorMessage, status = 400)
                except Exception:
                    return HttpResponse(ExceptionMessage, status = 400)
        else:
            return HttpResponse("AuthorizationError", status=401)
    else:
        return HttpResponse("Method not allowed on /offers.", status = 405)

@csrf_exempt
@sensitive_post_parameters()
def specificOffer(request, offerId):
    """ This view handles are requests made to /offer/<id> route. 
    When a GET request is made, information about the specific offer
    is displayed. When a PATCH request is made (only admin can patch
    and delete offers on website) specific offer information can
    be updated such as the discount amount, and description. When a
    DELETE request is made specific offers can be deleted from the 
    website."""
    if request.method == 'GET':
        try:
            # Gets the specific offer specified by url parameter
            specOffer = Offers.objects.all().values().filter(pk = offerId)[0]
            return JsonResponse(specOffer, safe = False,  content_type = 'application/json')
        
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)

    elif request.method == 'PATCH':
        if request.user.is_authenticated:
            try:
                if len(Users.objects.all().values().filter(
                    id= request.user.id, 
                    membership = "administrator"
                    )) == 0:
                    return HttpResponse("Unauthorized", status=403)
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status = 400)
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)

            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                try:
                    # If description is in json body, update description, and if
                    # offer_perc is in json body, update offer_perc of the specifeied
                    # offer
                    if 'description' in posted_data:
                        Offers.objects.filter(id= offerId).update(description= posted_data['description'])
                    if 'offer_perc' in posted_data:
                        Offers.objects.filter(id= offerId).update(offer_perc= posted_data['offer_perc'])

                    # returns updated info of offer
                    offerInfo = Offers.objects.all().values().filter(id= offerId)[0]
                    return JsonResponse(
                        offerInfo, 
                        safe = False, 
                        content_type = 'application/json', 
                        status = 201
                        )
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status=400)
                except KeyError:
                    return HttpResponse(KeyErrorMessage, status = 400)
                except Exception:
                    return HttpResponse(ExceptionMessage, status = 400)
        else:
            return HttpResponse("AuthorizationError", status=401)

    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            try:
                if len(Users.objects.all().values().filter(
                    id= request.user.id, 
                    membership = "administrator"
                    )) == 0:
                    return HttpResponse("Unauthorized", status=403)

                # Deletes the specified offer
                Offers.objects.filter(id= offerId).delete()
                return HttpResponse("The offer has been deleted.")
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
            
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
        else:
            return HttpResponse(AuthorizationError, status=401)

    else :
        return HttpResponse("Method not allowed on /offers/.", status = 405)


            
@csrf_exempt
@sensitive_post_parameters()
def theaterMovies(request, theater_id):
    """ This view handles all requests made to /theaters/<id>/tickets.
    When a GET request is made, all tickets available in the specific 
    theater will be displayed. When a POST (only admins can post and delete)
    request is made, new tickets can be added to the theater when infomation
    of about movie, price movie type, and time are provided. When a DELETE 
    request is made specific tickets can be deleted from the theater. Only
    tickets for the specified theater can be deleted.
    """
    current_user = request.user
    if request.method == "GET":
        try:
            # get all tickets
            all_movies = Tickets.objects.filter(
                theater = theater_id
                ).all().values('movie').distinct()

            movieList = []
            for movie in all_movies:
                movieList.append(Movies.objects.get(id = movie['movie']))

        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return all tickets data as a json object
            return render(
                request,
                '../templates/main/theaterMovies.html',
                {'movieList': movieList},
                status = 200
            )
    else:
        return HttpResponse(BadRequestMessage, status = 405)           

                
@csrf_exempt
@sensitive_post_parameters()
def addCart(request, theater_id, movie_id, ticket_id):

    if request.method == 'GET':
        try:
            form = AddCartForm()
            return render(request, '../templates/main/addCart.html', {'form': form}, status = 200)
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
        except KeyError:
            return HttpResponse(KeyErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)

    if(request.method == 'POST'): 
        try:     
            current_user = request.user
            if not current_user.is_authenticated:
                return HttpResponse(AuthorizationError, status = 401)

            form = AddCartForm(request.POST)
            if not form.is_valid():
                return HttpResponse("Bad login form.", status = 400)

            the_quantity = int(form.cleaned_data['quantity'])
            the_user = Users.objects.get(id = current_user.id)
            the_ticket = Tickets.objects.get(id = ticket_id)

            if(the_quantity > the_ticket.amount):
                error = "There Are Not Enough Tickets For This Movie Showing."
                form = AddCartForm()
                return render(request, '../templates/main/addCart.html', {'form': form, 'error': error}, status = 200)
            else:
                Tickets.objects.filter(id = ticket_id).update(amount = the_ticket.amount - the_quantity)
            
            if(current_user.membership == 'member'):
                the_offer = Offers.objects.get(offer_name = 'Membership')
            else:
                the_offer = Offers.objects.get(offer_name = 'No Offer')


            the_total_price = float(the_quantity) * float(the_ticket.price) * float(
                1 - the_offer.offer_perc)
 
            the_total_price = round(the_total_price, 2)

            new_cart = Cart.objects.create(
                user = the_user, 
                ticket = the_ticket, 
                quantity = the_quantity, 
                offer = the_offer, 
                total_price = the_total_price
                )

            new_cart.save()
            return HttpResponseRedirect("/cart")
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
        except KeyError:
            return HttpResponse(KeyErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)                   

    else:
        return HttpResponse("Method not allowed on /.", status = 405)





            



        
    

