from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class InfoField(serializers.Field):
    def to_representation(self, place):
        display = ''
        if place.gender:
            display += place.get_gender(place.gender) + ', '
        display += str(place.age) + _(' years old.')
        display += place.get_activity_type(place.activity_type).title() + _(' rest')
        return display
