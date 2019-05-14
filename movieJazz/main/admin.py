from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Theaters, Movies, Tickets, News, Reviews, Offers, Transactions

admin.site.register(Users, UserAdmin)
# Register your models here.
admin.site.register(Theaters)
admin.site.register(Movies)
admin.site.register(Tickets)
admin.site.register(News)
admin.site.register(Reviews)
admin.site.register(Offers)
admin.site.register(Transactions)
