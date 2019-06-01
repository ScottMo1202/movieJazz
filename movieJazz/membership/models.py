from django.db import models
from main.models import Users
from django.http import HttpResponse

# Create your models here.
class Membertransaction(models.Model):
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    membership = models.CharField(max_length = 50, null = False)
    total_price = models.IntegerField(null = False)
    date = models.DateTimeField(auto_now_add= True)


    def save(self, *args, **kwargs):
        if self.membership in ['member', 'seller'] and self.total_price in [20, 15, 120, 100]:
            super().save(*args, **kwargs)
        else:
            return HttpResponse('This is not a valid membership', status = 400) 
        