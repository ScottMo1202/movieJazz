from django.db import models
from django.http import HttpResponse
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Theaters(models.Model):
    name = models.CharField(required = True, max_length = 100, null = False)
    street_number = models.CharField(required = True, max_length = 10, null = False)
    street_name = models.CharField(required = True, max_length = 1000, null = False)
    city = models.CharField(required = True, max_length = 500, null = False)
    state = models.CharField(required = True, max_length = 2, null = False)
    post_code = models.CharField(required = True, max_length = 5, null = False)

class Memberships(models.Model):
    name = models.CharField(required = True, max_length = 100, null = False, unique = True)
    
    def save(self, *args, **kwargs):
        if self.name in ['administrator', 'member', 'normal']:
            super().save(*args, **kwargs)
        else:
            return HttpResponse('This is not a valid membership', status = 400) 

class Users(models.Model):
    username = models.CharField(required = True, max_length = 50, null = False, unique = True)
    password = models.CharField(required = True, max_length = 50, null = False)
    first_name = models.CharField(required = True, max_length = 100, null = False)
    last_name = models.CharField(required = True, max_length = 100, null = False)
    email = models.EmailField(required = True, unique = True, null = False)
    membership = models.ForeignKey(Memberships, default=lambda: Memberships.objects.get(id=1), on_delete=models.CASCADE)

class Movies(models.Model):
    name = models.CharField(required = True, max_length = 50, null = False)
    description = models.TextField(max_length = 5000, null = False)
    runtime = models.PositiveIntegerField(required = True,validators=[MinValueValidator(1), MaxValueValidator(500)])

class Tickets(models.Model):
    movie = models.ForeignKey(Movies, on_delete = models.CASCADE)
    time = models.DateTimeField(required = True)
    theater = models.ForeignKey(Theaters, on_delete = models.CASCADE)
    price = models.DecimalField(required = True, max_digits=5, decimal_places=2)
    
    REGULAR = 'RE'
    IMAX = 'IM'
    THREED = '3D'
    FOURD = '4D'
    RPX = 'RP'
    MOVIE_TYPE_CHOICES = (
        (REGULAR, 'Regular'),
        (IMAX, 'IMAX'),
        (THREED, '3D'),
        (RPX, 'RPX'),
        (FOURD, '4D')
    )
    movie_type = models.CharField(
        required = True,
        max_length=2,
        choices=MOVIE_TYPE_CHOICES,
        default=REGULAR
    )

class News(models.Model):
    body = models.TextField(required = True, max_length = 5000, null = False)
    movie = models.ForeignKey(Movies, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add= True)

class Reviews(models.Model):
    body = models.TextField(max_length = 1000)
    movie = models.ForeignKey(Movies, on_delete = models.CASCADE)
    
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    MOVIE_RATING_CHOICES = (
        (ONE, 'Terrible'),
        (TWO, 'Bad'),
        (THREE, 'Average'),
        (FOUR, 'Good'),
        (FIVE, 'Excellent')
    )
    rating = models.CharField(
        required = True,
        max_length=1,
        choices=MOVIE_RATING_CHOICES
    )

    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add= True)

class Offers(models.Model):
    offer_name = models.CharField(required = True, max_length = 150, null = False, unique = True)
    offer_perc = models.DecimalField(required = True, max_digits=2, decimal_places=2)
    description = models.CharField(required = True, max_length = 2000, null = False)

class Transactions(models.Model):
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField(required = True, validators=[MinValueValidator(1), MaxValueValidator(200)], null = False)
    offer = models.ForeignKey(Offers, default=lambda: Memberships.objects.get(id=1), on_delete = models.CASCADE)
    total_price = models.DecimalField(required = True, max_digits=6, decimal_places=2, null=False)
    date = models.DateTimeField(auto_now_add= True)

    def save(self, *args, **kwargs):
        qty = float(self.quantity)
        cost = float(Tickets.objects.get(id=self.ticket))
        disc = 1.0 - float(Offers.objects.get(id=self.offer))
        tot_price = float(self.total_price)
        if qty*cost*disc == tot_price :
            super().save(*args, **kwargs)
        else:
            return HttpResponse('Line Items Have Arithmatic Errors, Invalid Transaction', status = 400)
