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
    if request.method == 'GET':
        form = QuestionForm()
        return render(request, '../templates/contact/contactus.html', {'form': form}, status = 200)
    elif request.method == 'POST':
        form = QuestionForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Invalid registration request.", status = 400)
        else:
            
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
    if request.method == 'GET':
        try:
            question_list = list(Question.objects.all().values())
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            return render(request, '../templates/contact/questions.html', {"questionList": question_list, 'user': request.user}, status = 200)
    else:
        return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
def ansQuestion(request, question_id):
    if not request.user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    current_user = request.user
    # check if the user has right authorization
    if current_user.membership != 'administrator':
        return HttpResponse(AuthorizationError, status = 401)
    else:
        print(request.method)
        if request.method == 'GET':
            form = AnswerForm()
            return render(request, '../templates/contact/answer.html', {'form': form}, status = 200)
        elif request.method == 'POST':
            form = AnswerForm(request.POST)
            if not form.is_valid():
                return HttpResponse("Invalid registration request.", status = 400)
            else:
                try:
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
            
            




        

