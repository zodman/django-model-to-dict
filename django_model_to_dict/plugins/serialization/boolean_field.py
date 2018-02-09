from . import SerializationPlugin
from django.db.models import BooleanField
from django.conf import settings

class BooleanFieldSerializationPlugin(SerializationPlugin):
    field_type = BooleanField

    @staticmethod
    def serialize_field(field, model_instance):
        return field.value_from_object(model_instance)
