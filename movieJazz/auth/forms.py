from django import forms

class ReigistrationForm(forms.Form):
    username = forms.CharField(label = 'username', max_length = 50, required = True)
    password = forms.CharField(label = 'password', max_length = 50, 
               widget=forms.TextInput(attrs={'type' : 'password'}), required=True)
    passwordconf = forms.CharField(label = 'passwordconf', max_length = 50, 
               widget=forms.TextInput(attrs={'type' : 'password'}), required=True)
    first_name = forms.CharField(label = 'first_name', max_length = 30, required = True)
    last_name = forms.CharField(label = 'last_name', max_length = 30, required = True)
    email = forms.EmailField(required = True)

class SigninForm(forms.Form):
    username = forms.CharField(label = 'username', max_length = 50, required = True)
    password = forms.CharField(label = 'password', max_length = 50, 
               widget=forms.TextInput(attrs={'type' : 'password'}), required = True)