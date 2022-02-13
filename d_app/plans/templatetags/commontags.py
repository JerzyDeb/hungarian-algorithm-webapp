from django import template
register = template.Library()


@register.filter
def index(array, i):
    return array[i]


@register.filter
def get_name(queryset):
    return queryset.name


@register.filter
def get_surname(queryset):
    return queryset.surname

