from django.db import models
from main.models import Users, Tickets, Offers
from django.http import HttpResponse
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(200)], null = False)
    offer = models.ForeignKey(Offers, on_delete = models.CASCADE, null=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, null=False)

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