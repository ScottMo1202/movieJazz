from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Question
from main.models import Users
from django.db import DatabaseError
import json
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
import datetime
from .forms import QuestionForm, AnswerForm
# Create your views here.

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."
KeyErrorMessage = "Erros when accessing the object"
ExceptionMessage = "Some Exceptions Happened"
AuthorizationError = "Not Authorized"

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
def contact(request):
    """It only deals with two HTTP method: GET, POST. When GET, 
       the system will render a question form where the user 
       can post the question he wants to ask. When POST, it checks 
       all data filled in the form, create a new question model 
       based on the data and save it into the database.
    """
    if request.method == 'GET':
        form = QuestionForm()
        return render(request, '../templates/contact/contactus.html', {'form': form}, status = 200)
    elif request.method == 'POST':
        form = QuestionForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Invalid registration request.", status = 400)
        else:
            # retrieve the data from the form the user filled.
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            new_question = Question.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                subject = subject,
                body = body
            )
            new_question.save()
            return HttpResponse("Thank you for posting questions", status = 200)
    else:
        return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
def questions(request):
    """It only deals with one HTTP method GET, it will 
       list all questions and their answers to the screen.
    """
    if request.method == 'GET':
        try:
            # retrieve all questions from the database
            question_list = list(Question.objects.all().values())
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            return render(
                request, 
                '../templates/contact/questions.html', 
                {"questionList": question_list, 'user': request.user}, 
                status = 200
                )
    else:
        return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
def ansQuestion(request, question_id):
    """ It deals with GET and POST methods. When GET, 
        The system will render a form that allows the 
        administrator to provide the answer. When POST,
        the database will save the answer into the model
        of the specific question.
    """
    if not request.user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    current_user = request.user
    # check if the user has right authorization
    if current_user.membership != 'administrator':
        return HttpResponse(AuthorizationError, status = 401)
    else:
        print(request.method)
        # renders the form for providing answers
        if request.method == 'GET':
            form = AnswerForm()
            return render(
                request, 
                '../templates/contact/answer.html', 
                {'form': form}, 
                status = 200
                )
        elif request.method == 'POST':
            form = AnswerForm(request.POST)
            if not form.is_valid():
                return HttpResponse("Invalid registration request.", status = 400)
            else:
                try:
                    # save the answer to the database.
                    the_id = question_id
                    the_answer = form.cleaned_data['body']
                    the_question = Question.objects.filter(id = the_id).get()
                    the_question.answer = the_answer
                    the_question.save()
                except DatabaseError:
                    return HttpResponse(DatabaseErrorMessage, status = 400)
                except Exception:
                    return HttpResponse(ExceptionMessage, status = 400)
                else:
                    return HttpResponse('Thank you for answering', status = 201)
        else:
            return HttpResponse(BadRequestMessage, status = 405)
            
            




        

