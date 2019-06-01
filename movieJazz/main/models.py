from django.db import models
from django.http import HttpResponse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Theaters(models.Model):
    name = models.CharField(max_length = 100, null = False)
    street_number = models.CharField(max_length = 10, null = False)
    street_name = models.CharField(max_length = 1000, null = False)
    city = models.CharField(max_length = 500, null = False)
    state = models.CharField(max_length = 2, null = False)
    post_code = models.CharField(max_length = 5, null = False)
'''
class Memberships(models.Model):
    name = models.CharField(max_length = 100, null = False, unique = True)
    
    def save(self, *args, **kwargs):
        if self.name in ['administrator', 'member', 'normal']:
            super().save(*args, **kwargs)
        else:
            return HttpResponse('This is not a valid membership', status = 400) 
'''
class Users(AbstractUser):
    membership = models.CharField(max_length = 50, null = False, default = "normal")

    def save(self, *args, **kwargs):
        if self.membership in ['administrator', 'member', 'normal', 'seller']:
            super().save(*args, **kwargs)
        else:
            return HttpResponse('This is not a valid membership', status = 400) 

class Movies(models.Model):
    name = models.CharField(max_length = 50, null = False)
    description = models.TextField(max_length = 5000, null = False)
    runtime = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)])

class Tickets(models.Model):
    movie = models.ForeignKey(Movies, on_delete = models.CASCADE)
    time = models.DateTimeField(null = False)
    theater = models.ForeignKey(Theaters, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, null = False)
    
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
        max_length=2,
        choices=MOVIE_TYPE_CHOICES,
        default=REGULAR,
        null = False
    )

class News(models.Model):
    body = models.TextField(max_length = 5000, null = False)
    movies = models.ManyToManyField(Movies, null = False)
    date = models.DateTimeField(auto_now_add= True, null = False)

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
        max_length=1,
        choices=MOVIE_RATING_CHOICES,
        null = False
    )
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add= True)

class Offers(models.Model):
    offer_name = models.CharField(max_length = 150, null = False, unique = True)
    offer_perc = models.DecimalField(max_digits=2, decimal_places=2)
    description = models.CharField(max_length = 2000, null = False)

class Transactions(models.Model):
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(200)], null = False)
    offer = models.ForeignKey(Offers, on_delete = models.CASCADE, null=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    date = models.DateTimeField(auto_now_add= True)

    def save(self, *args, **kwargs):
        if self.offer is None:
            self.offer = Offers.objects.filter(name="No Offer").get()
        qty = float(self.quantity)
        cost = float(Tickets.objects.get(id=self.ticket.id).price)
        disc = 1.0 - float(Offers.objects.get(id=self.offer.id).offer_perc)
        tot_price = float(self.total_price)
        if round(qty*cost*disc, 2) == tot_price :
            super().save(*args, **kwargs)
        else:
            return HttpResponse('Line Items Have Arithmatic Errors, Invalid Transaction', status = 400)
