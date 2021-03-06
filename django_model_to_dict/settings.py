from django.conf import settings

DEFAULT_SERIALIZATION_PLUGINS = (
    'django_model_to_dict.plugins.serialization.imagefile_field.ImageFieldSerializationPlugin',
    'django_model_to_dict.plugins.serialization.date_field.DateFieldSerializationPlugin',
    'django_model_to_dict.plugins.serialization.datetime_field.DateTimeFieldSerializationPlugin',
    'django_model_to_dict.plugins.serialization.time_field.TimeFieldSerializationPlugin',
)
DEFAULT_SKIP = tuple()
DEFAULT_GROUPING = {}
DEFAULT_PREFIXES = tuple()
DEFAULT_PREFIX_SEPARATOR = '_'
DEFAULT_POSTFIXES = tuple()
DEFAULT_POSTFIX_SEPARATOR = '_'

TO_DICT_SERIALIZATION_PLUGINS = getattr(settings, 'TO_DICT_SERIALIZATION_PLUGINS', DEFAULT_SERIALIZATION_PLUGINS)
TO_DICT_SKIP = getattr(settings, 'TO_DICT_SKIP', DEFAULT_SKIP)
TO_DICT_GROUPING = getattr(settings, 'TO_DICT_GROUPING', DEFAULT_GROUPING)
TO_DICT_PREFIXES = getattr(settings, 'TO_DICT_PREFIXES', DEFAULT_PREFIXES)
TO_DICT_PREFIX_SEPARATOR = getattr(settings, 'TO_DICT_PREFIX_SEPARATOR', DEFAULT_PREFIX_SEPARATOR)
TO_DICT_POSTFIXES = getattr(settings, 'TO_DICT_POSTFIXES', DEFAULT_POSTFIXES)
TO_DICT_POSTFIX_SEPARATOR = getattr(settings, 'TO_DICT_POSTFIX_SEPARATOR', DEFAULT_POSTFIX_SEPARATOR)
