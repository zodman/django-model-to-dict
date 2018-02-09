from . import SerializationPlugin
from django.db.models import TimeField
from django.conf import settings

class TimeFieldSerializationPlugin(SerializationPlugin):
    field_type = TimeField

    @staticmethod
    def serialize_field(field, model_instance):
        file_obj = field.value_from_object(model_instance)
        if file_obj:
            for format in settings.TIME_INPUT_FORMATS:
                result = file_obj.strftime(format)
                if result:
                    return result

            return file_obj
        else:
            return ''
