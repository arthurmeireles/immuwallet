from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(name='cachebuster')
def cachebuster():
    version = settings.PROJECT_VERSION
    if version is None:
        version = '1'

    return '__v__={version}'.format(version=version)
