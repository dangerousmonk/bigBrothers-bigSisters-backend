import factory
from django.conf import settings
from datetime import date, timedelta
import random
from bbbs.common.choices import DiaryMarkChoices


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        strategy = factory.CREATE_STRATEGY

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@email.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}very-secret')
    first_name = factory.Sequence(lambda n: f'John{n}')
    last_name = factory.Sequence(lambda n: f'Doe{n}')
    role = factory.Iterator(['curator', 'moderator', 'moderator_reg'])
    gender = factory.Iterator(['M', 'F'])

    # TODO: make password hashed?


class DiaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'diary.Diary'

    place = factory.Sequence(lambda n: f'place{n}')
    meeting_date = factory.LazyAttribute(lambda o: date.today() - timedelta(days=7))
    description = factory.Sequence(lambda n: f'diary{n}')
    # TODO: image
    mark = factory.LazyFunction(
        lambda: random.choice(
            [DiaryMarkChoices.BAD, DiaryMarkChoices.GOOD, DiaryMarkChoices.NEUTRAL]
        )
    )
    author = factory.SubFactory(UserFactory)

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'common.Tag'

    name = 'tag'

