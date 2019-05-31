from django import forms

class SearchForm(forms.Form):
    input = forms.CharField(max_length = 1000, required = True)

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
    rating = forms.ChoiceField(required = True, choices = MOVIE_RATING_CHOICES, widget=forms.RadioSelect())
    text = forms.CharField(max_length = 5000, required = True)