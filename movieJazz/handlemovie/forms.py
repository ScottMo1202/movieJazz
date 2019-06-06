from django import forms

class SearchForm(forms.Form):
    input = forms.CharField(label = '',max_length = 1000, 
               widget=forms.TextInput(attrs={
                   'class' : 'form-control',
                   'placeholder': 'Search'
                   
                   }), required = True)

class ReviewForm(forms.Form):
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'

    MOVIE_RATING_CHOICES = (
        (ONE, 'Terrible'),
        (TWO, 'Bad'),
        (THREE, 'Average'),
        (FOUR, 'Good'),
        (FIVE, 'Excellent')
    )
    rating = forms.ChoiceField(label="", choices = MOVIE_RATING_CHOICES, required = True, 
                widget=forms.Select(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Subject'
                    
                    }))
    text = forms.CharField(label= '', max_length = 5000, required = True, 
                widget=forms.Textarea(attrs={
                    'class' : 'form-control',
                    'placeholder': 'Type Your Question Here.'
                    }))