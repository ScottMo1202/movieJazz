from django import forms

class QuestionForm(forms.Form):
    MOVIE = 'Movie'
    THEATER = 'Theater'
    OFFER = 'Offer'
    AUTH = 'Authentification'
    TRANS = 'Transaction'
    OTHER = 'Others'
    SUBJECT_CHOICE = (
        (MOVIE, 'Movie'),
        (THEATER, 'Theater'),
        (OFFER, 'Offer'),
        (AUTH, 'Authentification'),
        (TRANS, 'Transaction'),
        (OTHER, 'Others')
    )
    first_name = forms.CharField(label = '', max_length = 50, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'First Name'
                    
                    }), required = True)
    last_name = forms.CharField(label='',max_length = 50, 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Last Name'
                    
                    }), required = True)
    email = forms.EmailField(label = '', 
                widget=forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Email'
                    
                    }), required = True)
    subject = forms.ChoiceField(label="", choices = SUBJECT_CHOICE, required = True, 
                widget=forms.Select(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Subject'
                    
                    }))
    body = forms.CharField(label= '', max_length = 3000, required = True, 
                widget=forms.Textarea(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Type Your Question Here.'
                    
                    }))

class AnswerForm(forms.Form):
    body = forms.CharField( required = True, 
                widget=forms.Textarea(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Type Your Answer Here.',
                    'default': ''
                    }))