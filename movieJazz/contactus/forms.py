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
    first_name = forms.CharField(max_length = 50, required = True)
    last_name = forms.CharField(max_length = 50, required = True)
    email = forms.EmailField(required = True)
    subject = forms.ChoiceField(label="Subject", choices = SUBJECT_CHOICE, required = True, widget=forms.RadioSelect())
    body = forms.CharField(max_length = 1000, required = True)

class AnswerForm(forms.Form):
    question_id = forms.IntegerField(required = True)
    body = forms.CharField(max_length = 10000, required = True)