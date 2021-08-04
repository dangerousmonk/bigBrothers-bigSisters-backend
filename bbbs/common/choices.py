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


class BookColorChoices:
    LIGHT_BLUE = '#C8D1FF'
    ORANGE = '#FF8585'

    CHOICES = [
        (LIGHT_BLUE, _('light blue')),
        (ORANGE, _('orange')),
    ]


class RightColorChoices:
    YELLOW = '#F8D162'
    GREEN = '##8CDD94'
    ORANGE = '#FF8585'
    LIGHT_BLUE = '#C8D1FF'

    CHOICES = [
        (YELLOW, _('yellow')),
        (GREEN, _('green')),
        (ORANGE, _('orange')),
        (LIGHT_BLUE, _('light blue')),
    ]
