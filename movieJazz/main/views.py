from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    if request.method == 'GET':
        return render(request, '../templates/main/index.html', status = 200)
    else:
        return HttpResponse("Method not allowed on /.", status = 405)


