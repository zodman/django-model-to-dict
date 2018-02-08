from . import SerializationPlugin
from django.db.models import DateTimeField
from django.conf import settings

class DateTimeFieldSerializationPlugin(SerializationPlugin):
    field_type = DateTimeField

    @staticmethod
    def serialize_field(field, model_instance):
        file_obj = field.value_from_object(model_instance)
        if file_obj:
            for format in settings.DATETIME_INPUT_FORMATS:
                result = file_obj.strftime(format)
                if result:
                    return result
        else:
            return ''

