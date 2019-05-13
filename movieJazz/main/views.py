from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Theaters, Transactions, Tickets
from django.db import DatabaseError
import json
# Create your views here.

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."
KeyErrorMessage = "Erros when accessing the object"
ExceptionMessage = "Some Exceptions Happened"
AuthorizationError = "Not Authorized"

def home(request):
    if request.method == 'GET':
        return render(request, '../templates/main/index.html', status = 200)
    else:
        return HttpResponse("Method not allowed on /.", status = 405)

def jsonHandling(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JSONDecodeFailMessage
    except Exception:
        return JSONDecodeFailMessage
    else:
        return data



def theaters(request):
    if request.method == 'GET':
        theaters_data = []
        theaters_List = Theaters.objects.values()
        for each_theater in theaters_List:
            eachData = {}
            eachData['name'] = each_theater['name']
            eachData['street_number'] = each_theater['street_number']
            eachData['street_name'] = each_theater['steet_name']
            eachData['city'] = each_theater['city']
            eachData['state'] = each_theater['state']
            eachData['post_code'] = each_theater['post_code']
        return JsonResponse(theaters_data, safe = False, content_type = 'application/json')
    elif request.method == 'POST':
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        current_user = request.user
        if current_user.membership.name != 'administrator' or current_user.membership.name != 'seller':
            return HttpResponse(AuthorizationError, status = 401)
        else:
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
                new_theater = Theaters.objects.create(name = posted_data['name'], 
                street_number = posted_data['street_number'], street_name = posted_data['street_name'], 
                city = posted_data['city'], state = posted_data['state'], post_code = ['post_code'])
                new_theater.save()
                theater_id_list = Theaters.objects.values_list('id', flat = True)
                this_theater_id = Theaters.objects.values_list('id', flat = True).get(id = len(theater_id_list))
                this_theater_name = Theaters.objects.values_list('name', flat = True).get(id = len(theater_id_list))
                this_theater_street_number = Theaters.objects.values_list('street_number', flat = True).get(id = len(theater_id_list))
                this_theater_street_name = Theaters.objects.values_list('street_name', flat = True).get(id = len(theater_id_list))
                this_theater_city = Theaters.objects.values_list('city', flat = True).get(id = len(theater_id_list))
                this_theater_state = Theaters.objects.values_list('state', flat = True).get(id = len(theater_id_list))
                this_theater_post_code = Theaters.objects.values_list('post_code', flat = True).get(id = len(theater_id_list))
                new_theater_json = {'id': this_theater_id, 'name': this_theater_name, 
                                   'street_number': this_theater_street_number, 
                                   'street_name': this_theater_street_name,
                                   'city': this_theater_city, 'state': this_theater_state,
                                   'post_code': this_theater_post_code}
                return JsonResponse(new_theater_json, safe = False, content_type = 'application/json', status = 201)
    else:
        return HttpResponse(BadRequestMessage, status = 405)

def specificTheater(requests, theater_id):
    if request.method == 'GET':
        the_theater = Theaters.objects.filter(id = theater_id).get()
        the_theater_data = {"name": the_theater.name, 'street_number': the_theater.street_number, 
                           'street_name': the_theater.street_name, 'city': the_theater.city,
                           'state': the_theater.state, 'post_code': the_theater.post_code}
        return JsonResponse(the_theater_data, safe = False, content_type = 'application/json', status = 201)
    elif request.method == 'PATCH':
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        current_user = request.user
        if current_user.membership != 'administrator' or current_user.membership.name != 'seller':
            return HttpResponse(AuthorizationError, status = 403)
        else:
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            else:
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
            return JsonResponse(changed_data, safe = False, content_type = 'application/json', status = 201)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        if current_user.membership != 'administrator' or current_user.membership.name != 'seller':
            return HttpResponse(AuthorizationError, status = 403)
        the_theater.delete()
        return HttpResponse('Deleted', status = 200)
    else:
        return HttpResponse(BadRequestMessage, status = 405)
'''
def specificTicket(request):
    if not request.user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    else:
        if request.method == "GET":
'''

            
            

                






            



        
    

