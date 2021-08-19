from rest_framework import mixins, viewsets

from django.utils.translation import gettext_lazy as _
from django.contrib.admin import ModelAdmin

from django.contrib import admin
from .models import Tag


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
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_moderator_reg:
            return qs.filter(city=request.user.city)
        return qs

    def has_module_permission(self, request):
        return not request.user.is_anonymous

    def has_view_permission(self, request, obj=None):
        return not request.user.is_anonymous

    def has_add_permission(self, request):
        return not request.user.is_anonymous

    def has_change_permission(self, request, obj=None):
        return not request.user.is_anonymous

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_anonymous

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_moderator_reg:
            form.base_fields['city'].initial = request.user.city
            form.base_fields['city'].disabled = True
            form.base_fields['city'].help_text = _('Can add only in your city')
        return form
