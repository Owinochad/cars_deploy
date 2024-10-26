from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (TypeError, ValueError):
        return ''

@register.filter
def item_count(queryset):
    return queryset.count()

@register.filter
def add_class(field, css_class):
    """Add a class to a form field."""
    return field.as_widget(attrs={"class": css_class})
