from django.utils.translation import gettext_lazy as _


class TagChoices:
    EVENTS = 'events'
    PLACES = 'places'
    QUESTIONS = 'questions'
    RIGHTS = 'rights'
    BOOKS = 'books'
    MOVIES = 'movies'
    VIDEOS = 'videos'

    CHOICES = [
        (EVENTS, _('tag events')),
        (PLACES, _('tag places')),
        (QUESTIONS, _('tag questions')),
        (RIGHTS, _('tag rights')),
        (BOOKS, _('tag books')),
        (MOVIES, _('tag movies')),
        (VIDEOS, _('tag videos')),
    ]
