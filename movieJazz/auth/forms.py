from django import forms

class ReigistrationForm(forms.Form):
    username = forms.CharField(label = '', max_length = 50, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Username'
                    
                    }), required = True)
    password = forms.CharField(label = '',max_length = 50, 
               widget=forms.TextInput(attrs={
                   'type' : 'password',
                   'class' : 'form-control',
                   'placeholder': 'Password'
                   
                   }), required = True)
    passwordconf = forms.CharField(label = '',max_length = 50, 
               widget=forms.TextInput(attrs={
                   'type' : 'password',
                   'class' : 'form-control',
                   'placeholder': 'Confirm Password'
                   
                   }), required = True)
    first_name = forms.CharField(label = '', max_length = 30, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'First Name'
                    
                    }), required = True)
    last_name = forms.CharField(label = '', max_length = 30, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Last Name'
                    
                    }), required = True)
    email = forms.EmailField(label = '', 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Email'
                    
                    }), required = True)

class SigninForm(forms.Form):
    username = forms.CharField(label = '', max_length = 50, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Username'
                    
                    }), required = True)
    password = forms.CharField(label = '',max_length = 50, 
               widget=forms.TextInput(attrs={
                   'type' : 'password',
                   'class' : 'form-control',
                   'placeholder': 'Password'
                   
                   }), required = True)