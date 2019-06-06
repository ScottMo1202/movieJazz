from django.db import models

# Create your models here.
class Question(models.Model):
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

    first_name = models.CharField(max_length = 50, null = False)
    last_name = models.CharField(max_length = 50, null = False)
    email = models.EmailField(null = False)
    subject = models.CharField(max_length = 100, choices = SUBJECT_CHOICE, null = False)
    body = models.CharField(max_length = 1000, null = False)
    answer = models.CharField(max_length = 3000, null = True)