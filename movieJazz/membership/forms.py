from django import forms

class CheckoutForm(forms.Form):
    Yes = 'Yes'
    No = 'No'
    AUTO_CHOICES = (
        (Yes, 'Yes'),
        (No, 'No')
    )
    auto_renew = forms.ChoiceField(label = 'auto_renew', choices = AUTO_CHOICES, required = True, widget=forms.RadioSelect())
    name_on_card = forms.CharField(max_length = 500, required = True)
    billing_address = forms.CharField(max_length = 1000, required = True)
    number_card = forms.CharField(max_length = 1000, required = True)
    csv_code = forms.CharField(max_length = 1000, required = True)
