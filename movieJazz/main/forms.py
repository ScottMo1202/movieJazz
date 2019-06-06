from django import forms

class AddCartForm(forms.Form):
    quantity = forms.IntegerField(label = '', 
               widget=forms.NumberInput(attrs={
                   'class' : 'form-control',
                   'placeholder': 'Quantity'
                   
                   }), required = True)
