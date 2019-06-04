from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from main.models import Movies, Users, Reviews
from .forms import SearchForm, ReviewForm
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
def movies(request):
    """ This view handles all requests made to /movies route. When a GET
    request is made, all movies will be displayed as a webpage, with all
    movie information such as name, description, and runtime. When a POST
    request is made (only admins can make posts, and add movies to database)
    new movie entries can be added to the website, with information like
    name, description, and runtime specified. """
    if request.method == 'GET':
        try:
            # get all movies and return all movie data in the template
            moviesList = list(Movies.objects.all().values()) 
            return render(
                request, 
                '../templates/movies/movies.html', 
                {'movieList': moviesList}, 
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
                    # create a new movie
                    newMovie = Movies.objects.create(name = posted_data['name'], 
                    description = posted_data['description'], runtime = posted_data['runtime'])
                    newMovie.save()
                    movieInfo = Movies.objects.all().values().filter(pk=newMovie.pk)[0]
                    # return the newly created movie as a json object
                    return JsonResponse(
                        movieInfo, 
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
        return HttpResponse("Method not allowed on /movies.", status = 405)


@csrf_exempt
@sensitive_post_parameters()
def specificMovie(request, movieId):
    """ This view handles all requests made to /movies/<id> route.
    When a GET request is made, information about the specific movie
    is displayed. When a PATCH request is made (only admins can
    patch and delete movie entries) information about the specific 
    movie can be changed, such as description and runtime. When a 
    DELETE request is made specific movies can be deleted from the
    website."""
    if request.method == 'GET':
            # gets specific movies based off of url parameter
            specMovie = Movies.objects.all().values().filter(pk = movieId)[0]
            all_reviews = list(Reviews.objects.filter(movie__id = specMovie['id']).all().values())
            return render(request, '../templates/movies/specMovie.html', {'movie': specMovie, 'reviewList': all_reviews}, status = 200)
    elif request.method == 'PATCH':
        if request.user.is_authenticated:

            # checks to see if user is admin or not
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
                    # if description is in the JSON body, then update description 
                    # for the specific movie.
                    if 'description' in posted_data:
                        Movies.objects.filter(id= movieId).update(description= posted_data['description'])
                    movieInfo = Movies.objects.all().values().filter(id= movieId)[0]
                    
                    #returns the updated information of specific movie 
                    return JsonResponse(
                        movieInfo, 
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

                # deletes specific movie from the data base
                Movies.objects.filter(id= movieId).delete()
                return HttpResponse("The movie has been deleted.")
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
        else:
            return HttpResponse("AuthorizationError", status=401)

    else :
        return HttpResponse("Method not allowed", status = 405)

@csrf_exempt
def search(request):
  if request.method == 'GET':
      form = SearchForm()
      return render(request, '../templates/movies/search.html', {'form': form}, status = 200)
  elif request.method == 'POST':
      form = SearchForm(request.POST)
      if not form.is_valid():
          return HttpResponse("Invalid registration request.", status = 400)
      else:
          try:
            query = str(form.cleaned_data['input'])
            the_result = list(Movies.objects.filter(name__icontains = query).all().values())
            if (len(the_result) == 0):
                return render(request, '../templates/movies/searchResult.html', {'movieList': the_result, 'query': query}, status = 200)
            else:
                return render(request, '../templates/movies/searchResult.html', {'movieList': the_result, 'query': query}, status = 200)
          except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
          except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
  else:
      return HttpResponse("Method not allowed", status = 405)

@csrf_exempt
def review(request, movie_id):
    if request.method == 'GET':
        form = ReviewForm()
        return render(request, '../templates/movies/review.html', {'form': form}, status = 200)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse("AuthorizationError", status=401)
        else:
            form = ReviewForm(request.POST)
            if not form.is_valid():
                return HttpResponse("Invalid registration request.", status = 400)
            else:
                try:
                    rating = form.cleaned_data['rating']
                    text = form.cleaned_data['text']
                    the_movie = Movies.objects.filter(id = movie_id).get()
                    new_review = Reviews.objects.create(
                        body = text, 
                        movie = the_movie, 
                        rating = rating,
                        user = request.user
                    )
                    new_review.save()
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status=400)
                except Exception:
                    return HttpResponse(ExceptionMessage, status = 400)
                else:
                    return HttpResponse('Thanks for rating!', status = 201)
    else:
        return HttpResponse("Method not allowed", status = 405)
