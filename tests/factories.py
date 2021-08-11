import factory
from factory import fuzzy
from django.conf import settings
from datetime import date, timedelta
import random
from bbbs.common.choices import DiaryMarkChoices, UserRoleChoices, UserGenderChoices


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        strategy = factory.CREATE_STRATEGY

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@email.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}very-secret')
    first_name = factory.Sequence(lambda n: f'John{n}')
    last_name = factory.Sequence(lambda n: f'Doe{n}')
    role = factory.Iterator([UserRoleChoices.CURATOR, UserRoleChoices.MODERATOR])
    gender = factory.Iterator([UserGenderChoices.MALE, UserGenderChoices.FEMALE])

    # TODO: make password hashed?


class DiaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'diary.Diary'
    place = factory.Sequence(lambda n: f'place{n}')
    meeting_date = factory.Sequence(lambda n: date(2021, 7,1) + timedelta(days=n))
    description = factory.Faker('text')
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
