from django import forms

class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(required = True)


class CartDeleteForm(forms.Form):
    cart_id = forms.IntegerField(required = True)


class AddOffer(forms.Form):
    offer_id = forms.IntegerField(required = True)


class CartForm(forms.Form):
    name_on_card = forms.CharField(label = '', max_length = 500, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Name on Card' 
                    }), required = True)

    billing_address = forms.CharField(label = '', max_length = 1000, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Billing Address' 
                    }), required = True)


    number_card = forms.CharField(label = '', max_length = 1000, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Card Number' 
                    }), required = True)

    csv_code = forms.CharField(label = '', max_length = 1000, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'CSV Code' 
                    }), required = True)
