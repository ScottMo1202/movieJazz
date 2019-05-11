from django.db import models
from django.http import HttpResponse

def validate_membership_name(name):
    if not name in ['administrator', 'member', 'normal']:
        return HttpResponse('This is not a valid membership', status = 400)

# Create your models here.
class MovieTypes(models.Model):
    name = models.CharField(required = True, unique = True, max_length = 22, null = False)

class Theaters(models.Model):
    name = models.CharField(required = True, max_length = 100, null = False)
    street_number = models.CharField(required = True, max_length = 10, null = False)
    street_name = models.CharField(required = True, max_length = 1000, null = False)
    city = models.CharField(required = True, max_length = 500, null = False)
    state = models.CharField(required = True, max_length = 2, null = False)
    post_code = models.CharField(required = True, max_length = 5, null = False)

class Memberships(models.Model):
    name = models.CharField(required = True, max_length = 100, null = False, unique = True, validator = [validate_membership_name], default = "normal")

class Users(models.Model):
    username = models.CharField(required = True, max_length = 150, null = False, unique = True)
    password = models.CharField(required = True, max_length = 200, null = False)
    first_name = models.CharField(required = True, max_length = 100, null = False)
    last_name = models.CharField(required = True, max_length = 100, null = False)
    email = models.EmailField(required = True, unique = True, null = False)
    membership = models.ForeignKey(Memberships, on_delete=models.CASCADE)

class Movies(models.Model):
    name = models.CharField(required = True, max_length = 50, null = False)
    description = models.CharField(max_length = 2000, null = False)
    movie_type = models.ForeignKey(MovieTypes, on_delete=models.CASCADE)
    length = models.DurationField()

class Tickets(models.Model):
    movie = models.ForeignKey(Movies, on_delete = models.CASCADE)
    time = models.DateTimeField()
    theater = models.ForeignKey(Theaters, on_delete = models.CASCADE)
    price = models.DecimalField()
    movie_type = models.ForeignKey(MovieTypes, on_delete = models.CASCADE)

