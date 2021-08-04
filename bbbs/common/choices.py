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
        (EVENTS, _('tag for events')),
        (PLACES, _('tag for places')),
        (QUESTIONS, _('tag for questions')),
        (RIGHTS, _('tag for rights')),
        (BOOKS, _('tag for books')),
        (MOVIES, _('tag for movies')),
        (VIDEOS, _('tag for videos')),
    ]
