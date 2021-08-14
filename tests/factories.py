import random
from datetime import date, timedelta

from django.conf import settings

import factory

from bbbs.common.choices import (BookColorChoices, DiaryMarkChoices,
                                 RightColorChoices, UserGenderChoices,
                                 UserRoleChoices)


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
    meeting_date = factory.Sequence(lambda n: date(2021, 7, 1) + timedelta(days=n))
    description = factory.Faker('text')
    # image = factory.django.ImageField(width=1024, height=768)
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


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'books.Book'

    title = factory.Sequence(lambda n: f'book{n}')
    author = factory.Sequence(lambda n: f'author{n}')
    year = factory.LazyFunction(
        lambda: random.choice(
            [2010, 2012, 1999]
        )
    )
    description = factory.Faker('text')
    color = factory.LazyFunction(
        lambda: random.choice(
            [BookColorChoices.ORANGE, BookColorChoices.LIGHT_BLUE]
        )
    )
    url = factory.Faker('url')

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'common.City'

    name = factory.Sequence(lambda n: f'city-{n}')
    is_primary = factory.LazyFunction(lambda: random.choice([True, False]))


def get_random_color():
    color_choices = [option[0] for option in RightColorChoices.CHOICES]
    return random.choice(color_choices)


class RightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'rights.Right'

    title = factory.Sequence(lambda n: f'right title-{n}')
    description = factory.Sequence(lambda n: f'right description-{n}')
    text = factory.Faker('text')
    color = factory.LazyFunction(get_random_color)
    # image = factory.django.ImageField(width=1024, height=768)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'articles.Article'

    title = factory.Sequence(lambda n: f'article title-{n}')
    author_info = factory.Sequence(lambda n: f'famous author-{n}')
    article_url = factory.Faker('url')
    content = factory.Faker('text')
    # image = factory.django.ImageField(width=1024, height=768)


class StoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'story.Story'

    title = factory.Sequence(lambda n: f'story title-{n}')
    child_name = factory.Sequence(lambda n: f'Child-{n}')
    friends_since = factory.Sequence(lambda n: date(2021, 6, 1) + timedelta(days=n))
    author = factory.SubFactory(UserFactory)
    intro = factory.Sequence(lambda n: f'story intro-{n}')
    text = factory.Faker('text')
    quote = factory.Sequence(lambda n: f'story quote-{n}')
    image = factory.django.ImageField(width=1024, height=768)
