from django.utils.translation import gettext_lazy as _


class UserRoleChoices:
    ADMIN = 'admin'
    MODERATOR_REG = 'moderator_reg'
    MODERATOR = 'moderator'
    MENTOR = 'mentor'
    CURATOR = 'curator'

    CHOICES = [
        (ADMIN, _('Administrator')),
        (MODERATOR_REG, _('Regional moderator')),
        (MODERATOR, _('Moderator')),
        (MENTOR, _('Mentor')),
        (CURATOR, _('Curator')),
    ]


class UserGenderChoices:
    MALE = 'M'
    FEMALE = 'F'

    CHOICES = [
        (MALE, _('Male',)),
        (FEMALE, _('Female',)),
    ]


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
    GREEN = '#8CDD94'
    ORANGE = '#FF8585'
    LIGHT_BLUE = '#C8D1FF'

    CHOICES = [
        (YELLOW, _('yellow')),
        (GREEN, _('green')),
        (ORANGE, _('orange')),
        (LIGHT_BLUE, _('light blue')),
    ]


class DiaryMarkChoices:
    GOOD = 'good'
    BAD = 'bad'
    NEUTRAL = 'neutral'

    CHOICES = [
        (GOOD, _('good')),
        (BAD, _('bad')),
        (NEUTRAL, _('neutral')),
    ]


class RegionISOCodeChoices:
    MOSCOW = 'RU-MOW'
    MOSCOW_REGION = 'RU-MOS'
    SAINT_PETERSBURG = 'RU-SPE'
    LENINGRADSKAYA = 'RU-LEN'
    TVERSKAYA = 'RU-TVE'
    SVERDLOVSKAYA = 'RU-SVE'
    TYUMENSKAYA = 'RU-TYU'
    KOSTROMSKAYA = 'RU-KOS'
    BASHKARSTAN = 'RU-BA'
    YARASLAVSKOYA = 'RU-YAR'
    RYAZANSKAYA = 'RU-RYA'

    CHOICES = [
        (MOSCOW, _('Moscow')),
        (MOSCOW_REGION, _('Moskovskaya oblast')),
        (SAINT_PETERSBURG, _('Saint Petersburg')),
        (LENINGRADSKAYA, _('Leningradskaya oblast')),
        (TVERSKAYA, _('Tverskaya oblast')),
        (SVERDLOVSKAYA, _('Sverdlovskaya oblast')),
        (TYUMENSKAYA, _('Tyuemenskaya oblast')),
        (KOSTROMSKAYA, _('Kostromskaya oblast')),
        (BASHKARSTAN, _('Bashkarstan republic')),
        (YARASLAVSKOYA, _('Yaroslavskaya oblast')),
        (RYAZANSKAYA, _('Ryazanskaya oblast')),
    ]
