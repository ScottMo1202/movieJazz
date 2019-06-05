from django import forms

class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(required = True)


class CartDeleteForm(forms.Form):
    cart_id = forms.IntegerField(required = True)


class AddOffer(forms.Form):
    offer_id = forms.IntegerField(required = True)


class CartForm(forms.Form):
    name_on_card = forms.CharField(max_length = 500, required = True)
    billing_address = forms.CharField(max_length = 1000, required = True)
    number_card = forms.CharField(max_length = 1000, required = True)
    csv_code = forms.CharField(max_length = 1000, required = True)
