from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Theaters, Transactions, Tickets, Movies, Users, Offers
from django.db import DatabaseError
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

def defaultOffer():
    """ This will create an offer with 0% off, which is specifically for no offer used.
    The offer will only be created if it does not exist already. """

    # Checking if general channel exists
    if len(Offers.objects.all().values().filter(offer_name="No Offer", offer_perc=.00, description = "No Offer")) == 0:
        
        # Try to create admin user if it does not already exist
        try:
            offer = Offers.objects.create(offer_name = "No Offer", offer_perc =.00 , description = "No Offer")
            offer.save()
        
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
defaultOffer()

@csrf_exempt
@sensitive_post_parameters()
def home(request):
    if request.method == 'GET':
        return render(request, '../templates/main/index.html', status = 200)
    else:
        return HttpResponse("Method not allowed on /.", status = 405)

@csrf_exempt
@sensitive_post_parameters()
def jsonHandling(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JSONDecodeFailMessage
    except Exception:
        return JSONDecodeFailMessage
    else:
        return data


@csrf_exempt
@sensitive_post_parameters()
def theaters(request):
    if request.method == 'GET':
        try:
            theater_list = list(Theaters.objects.all().values())
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        else:
            return render(request, '../templates/main/theaters.html', {'theaters': theater_list} ,status = 200)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        current_user = request.user
        if current_user.membership != 'administrator' and current_user.membership != 'seller':
            return HttpResponse(AuthorizationError, status = 401)
        else:
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                try:
                    new_theater = Theaters.objects.create(name = posted_data['name'], 
                    street_number = posted_data['street_number'], street_name = posted_data['street_name'], 
                    city = posted_data['city'], state = posted_data['state'], post_code = posted_data['post_code'])
                    new_theater.save()
                    new_theater_info = Theaters.objects.all().values().filter(pk = new_theater.pk)[0]
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status = 400)
                except KeyError:
                    return HttpResponse(KeyErrorMessage, status = 400)
                else:
                    return JsonResponse(new_theater_info, safe = False, content_type = 'application/json', status = 201)
    else:
        return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
@sensitive_post_parameters()
def specificTheater(request, theater_id):
    if request.method == 'GET':
        try: 
            the_theater = Theaters.objects.filter(id = theater_id).get()
            the_theater_data = {"name": the_theater.name, 'street_number': the_theater.street_number, 
                            'street_name': the_theater.street_name, 'city': the_theater.city,
                            'state': the_theater.state, 'post_code': the_theater.post_code}
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        else:
            return JsonResponse(the_theater_data, safe = False, content_type = 'application/json', status = 201)
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
                else:
                    return JsonResponse(changed_data, safe = False, content_type = 'application/json', status = 201)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        if request.user.membership != 'administrator' and request.user.membership.name != 'seller':
            return HttpResponse(AuthorizationError, status = 403)
        try:
            Theaters.objects.filter(id= theater_id).delete()
        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        else:
            return HttpResponse('Deleted', status = 200)
    else:
        return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
@sensitive_post_parameters()
def tickets(request, theater_id):
    current_user = request.user
    if request.method == "GET":
        try:
            all_tickets = list(Tickets.objects.filter(theater = theater_id).all().values())
        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        else:
            return JsonResponse(all_tickets, safe = False, content_type = 'application/json', status = 201)
    
    elif request.method == 'POST':
        if not current_user.is_authenticated:
            return HttpResponse(AuthorizationError, status = 401)
        
        if current_user.membership == 'administrator':
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            try:
                the_ticket_movie = Movies.objects.filter(id = posted_data['movie']).get()
                the_ticket_theater = Theaters.objects.filter(id = theater_id).get()
                the_ticket_time = posted_data['time']
                the_ticket_price = posted_data['price']
                the_ticket_movie_type = posted_data['movie_type']
                new_ticket = Tickets.objects.create(movie = the_ticket_movie, time = the_ticket_time,
                            theater = the_ticket_theater, price = the_ticket_price,
                            movie_type = the_ticket_movie_type)
                new_ticket.save()
                ticketInfo = Tickets.objects.all().values().filter(pk = new_ticket.pk)[0]
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
            else:
                return JsonResponse(ticketInfo, safe = False, content_type = 'application/json', status = 201)
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
                toBeDeleted = Tickets.objects.filter(id = posted_data['id'], theater= theater_id)
                if toBeDeleted is None:
                    return HttpResponse('Ticket not available in Theater.', status = 200)
                toBeDeleted.delete()
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
            else:
                return HttpResponse('Ticket Deleted', status = 200)
        else:
            return HttpResponse(AuthorizationError, status = 403)
    else:
        return HttpResponse(BadRequestMessage, status = 405)


@csrf_exempt
@sensitive_post_parameters()
def transactions(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        if request.method == 'GET':
            try:
                transaction_list = list(Transactions.objects.all().values().filter(user= request.user.id))
                returnList = []
                for tran in transaction_list:
                    curTran = {}
                    curTran['movie'] = tran.ticket.movie.name
                    curTran['quantity'] = tran.quantity
                    curTran['total_price'] = tran.total_price
                    curTran['date'] = tran.date
                    returnList.append(curTran)
                return JsonResponse(returnList, safe = False, content_type = 'application/json')
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
                
        
        elif request.method == 'POST':
            if current_user.membership == 'administrator':
                posted_data = jsonHandling(request)
                if posted_data == JSONDecodeFailMessage:
                    return HttpResponse(JSONDecodeFailMessage, status = 400)
                try:
                    the_user = Users.objects.filter(id = posted_data['user']).get()
                    the_ticket = Tickets.objects.filter(id = posted_data['ticket']).get()
                    the_quantity = posted_data['quantity']
                    offer = Offers.objects.filter(id = posted_data['offer']).get()
                    the_total_price = float(the_quantity) * float(the_ticket.price) * float(1 - offer.offer_perc)
                    the_total_price = round(the_total_price, 2)
                    new_transaction = Transactions.objects.create(user = the_user, ticket = the_ticket,
                                        quantity = the_quantity, offer = offer, total_price = the_total_price)
                    new_transaction.save()
                    transaction_info = Transactions.objects.all().values().filter(pk = new_transaction.pk)[0]
                    
                except DatabaseError:
                    return HttpResponse(DatabaseError, status = 400)
                except KeyError:
                    return HttpResponse(DatabaseError, status = 400)
                else:
                    return JsonResponse(transaction_info, safe = False, content_type = 'application/json', status = 201)
            else:
                return HttpResponse(AuthorizationError, status = 403)
        
        elif request.method == 'PATCH':
            if current_user.membership == 'administrator':
                posted_data = jsonHandling(request)
                if posted_data == JSONDecodeFailMessage:
                    return HttpResponse(JSONDecodeFailMessage, status = 400)
                if 'id' in posted_data:
                    curTran = Transactions.objects.filter(id=posted_data['id'])
                    if 'quantity' in posted_data:
                        curTran.update(quantity= posted_data['quantity'])
                    if 'offer' in posted_data:
                        newDisc = Offers.objects.get(id=posted_data['offer'])
                        curTran.update(offer= newDisc)
                    
                    the_total_price = float(curTran.get().quantity) * float(curTran.get().ticket.price) * float(1 - curTran.get().offer.offer_perc)
                    the_total_price = round(the_total_price, 2)
                    curTran.update(total_price= the_total_price)

                    tranInfo = Transactions.objects.all().values().filter(id= posted_data['id'])[0]
                    return JsonResponse(tranInfo, safe = False, content_type = 'application/json', status = 201)

                else:
                    return HttpResponse(BadRequestMessage, status = 405)
            else:
                return HttpResponse(AuthorizationError, status = 403)
        
        elif request.method == 'DELETE':
            if current_user.membership == 'administrator':
                posted_data = jsonHandling(request)
                if posted_data == JSONDecodeFailMessage:
                    return HttpResponse(JSONDecodeFailMessage, status = 400)
                try:
                    Transactions.objects.filter(id = posted_data['id']).delete()
                except DatabaseError:
                    return HttpResponse(DatabaseError, status = 400)
                else:
                    return HttpResponse('Transaction Deleted', status = 200)
            else:
                return HttpResponse(AuthorizationError, status = 403)    
        else:
            return HttpResponse(BadRequestMessage, status = 405)
                
@csrf_exempt
@sensitive_post_parameters()
def movies(request):
    if request.method == 'GET':
        try:
            moviesList = list(Movies.objects.all().values()) 
            return JsonResponse(moviesList, safe = False,  content_type = 'application/json')
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
    
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if len(Users.objects.all().values().filter(id= request.user.id, membership = "administrator")) == 0:
                return HttpResponse("Unauthorized", status=403)
            
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                try:
                    newMovie = Movies.objects.create(name = posted_data['name'], 
                    description = posted_data['description'], runtime = posted_data['runtime'])
                    newMovie.save()
                    movieInfo = Movies.objects.all().values().filter(pk=newMovie.pk)[0]
                    return JsonResponse(movieInfo, safe = False, content_type = 'application/json', status = 201)
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status=400)
        else:
            return HttpResponse("AuthorizationError", status=401)
    else:
        return HttpResponse("Method not allowed on /movies.", status = 405)

@csrf_exempt
@sensitive_post_parameters()
def specificMovie(request, movieId):
    if request.method == 'GET':
        try:
            specMovie = Movies.objects.all().values().filter(pk = movieId)[0]
            return JsonResponse(specMovie, safe = False,  content_type = 'application/json')
        
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)

    elif request.method == 'PATCH':
        if request.user.is_authenticated:
            if len(Users.objects.all().values().filter(id= request.user.id, membership = "administrator")) == 0:
                return HttpResponse("Unauthorized", status=403)
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                try:
                    if 'description' in posted_data:
                        Movies.objects.filter(id= movieId).update(description= posted_data['description'])
                    movieInfo = Movies.objects.all().values().filter(id= movieId)[0]
                    return JsonResponse(movieInfo, safe = False, content_type = 'application/json', status = 201)
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status=400)
        else:
            return HttpResponse("AuthorizationError", status=401)

    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            if len(Users.objects.all().values().filter(id= request.user.id, membership = "administrator")) == 0:
                return HttpResponse("Unauthorized", status=403)
            try:
                Movies.objects.filter(id= movieId).delete()
                return HttpResponse("The movie has been deleted.")
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
        else:
            return HttpResponse("AuthorizationError", status=401)

    else :
        return HttpResponse("Method not allowed on /movies/.", status = 405)

@csrf_exempt
@sensitive_post_parameters()
def users(request):
    if request.user.is_authenticated:
        if len(Users.objects.all().values().filter(id= request.user.id, membership = "administrator")) == 0:
            return HttpResponse("Unauthorized", status=403)
        if request.method == 'GET':
            try:
                userList = list(Users.objects.all().values()) 
                return JsonResponse(userList, safe = False,  content_type = 'application/json')
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
        else :
            return HttpResponse("Method not allowed on /users.", status = 405)
    else:
        return HttpResponse(AuthorizationError, status=401)


@csrf_exempt
@sensitive_post_parameters()
def offers(request):
    if request.method == 'GET':
        try:
            offersList = list(Offers.objects.all().values()) 
            return JsonResponse(offersList, safe = False,  content_type = 'application/json')
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)
    
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if len(Users.objects.all().values().filter(id= request.user.id, membership = "administrator")) == 0:
                return HttpResponse("Unauthorized", status=403)
            
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                try:
                    newOffer = Offers.objects.create(offer_name = posted_data['offer_name'], 
                    offer_perc = posted_data['offer_perc'], description = posted_data['description'])
                    newOffer.save()
                    offerInfo = Offers.objects.all().values().filter(pk=newOffer.pk)[0]
                    return JsonResponse(offerInfo, safe = False, content_type = 'application/json', status = 201)
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status=400)
        else:
            return HttpResponse("AuthorizationError", status=401)
    else:
        return HttpResponse("Method not allowed on /offers.", status = 405)

@csrf_exempt
@sensitive_post_parameters()
def specificOffer(request, offerId):
    if request.method == 'GET':
        try:
            specOffer = Offers.objects.all().values().filter(pk = offerId)[0]
            return JsonResponse(specOffer, safe = False,  content_type = 'application/json')
        
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)

    elif request.method == 'PATCH':
        if request.user.is_authenticated:
            if len(Users.objects.all().values().filter(id= request.user.id, membership = "administrator")) == 0:
                return HttpResponse("Unauthorized", status=403)
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                try:
                    if 'description' in posted_data:
                        Offers.objects.filter(id= offerId).update(description= posted_data['description'])
                    if 'offer_perc' in posted_data:
                        Offers.objects.filter(id= offerId).update(offer_perc= posted_data['offer_perc'])

                    offerInfo = Offers.objects.all().values().filter(id= offerId)[0]
                    return JsonResponse(offerInfo, safe = False, content_type = 'application/json', status = 201)
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status=400)
        else:
            return HttpResponse("AuthorizationError", status=401)

    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            if len(Users.objects.all().values().filter(id= request.user.id, membership = "administrator")) == 0:
                return HttpResponse("Unauthorized", status=403)
            try:
                Offers.objects.filter(id= offerId).delete()
                return HttpResponse("The offer has been deleted.")
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
        else:
            return HttpResponse(AuthorizationError, status=401)

    else :
        return HttpResponse("Method not allowed on /offers/.", status = 405)


            
            

                






            



        
    

