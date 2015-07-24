from django import template

register = template.Library()


# example: {{ request.resolver_match.url_name|menu_active:'url-name-a, url-name-b, url-name-c' }}
@register.filter
def menu_active(value, url_names=''):
    url_names = url_names.replace(' ', '').split(',')
    return 'active' if value in url_names else None

