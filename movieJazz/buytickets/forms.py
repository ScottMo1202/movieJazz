from django import forms

class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(required = True)