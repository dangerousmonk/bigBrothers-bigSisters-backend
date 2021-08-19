from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from rest_framework import mixins, viewsets

from .models import City, Tag


class ListRetrieveCreateUpdateMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ListRetreiveCreateDestroyMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TagAdminMixin(ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            model_plural = self.model._meta.verbose_name_plural.lower()
            kwargs['queryset'] = Tag.objects.filter(model=model_plural)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    @admin.display(description=_('tags'))
    def get_tags(self, obj):
        qs = obj.list_tags()
        if qs:
            return list(qs)


class RegModeratorAdminMixin(ModelAdmin):
    # Allow region moderator to see and add instances related to his city region

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_moderator_reg:
            region_cities = request.user.city.region.cities.all()
            return qs.filter(city__in=region_cities)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'city' and request.user.is_moderator_reg:
            kwargs['queryset'] = City.objects.filter(region=request.user.city.region)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
