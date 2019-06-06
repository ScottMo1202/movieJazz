from django import forms

class CheckoutForm(forms.Form):
    Yes = 'Yes'
    No = 'No'
    AUTO_CHOICES = (
        (Yes, 'Yes'),
        (No, 'No')
    )
    auto_renew = forms.ChoiceField(label="", choices = AUTO_CHOICES, required = True, 
        widget=forms.Select(attrs={
            'class' : 'form-control',
            'placeholder': 'Yes/No'
            
            }))
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
