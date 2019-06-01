from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from main.models import Theaters, Transactions, Tickets, Movies, Users, Offers
from .forms import TicketPurchaseForm
from django.db import DatabaseError
import json
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
import datetime
# Create your views here.