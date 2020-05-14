"""
API helpers for django-rest-framework.
"""

from rest_framework import serializers


class FieldPermissionSerializerMixin:
    """
    ModelSerializer logic for marking fields as ``read_only=True`` when a user is found not to have
    change permissions.
    """

    def __init__(self, *args, **kwargs):
        super(FieldPermissionSerializerMixin, self).__init__(*args, **kwargs)

        user = self.context['request'].user
        model = self.Meta.model
        model_field_names = [f.name for f in model._meta.get_fields()]  # this might be too broad

        # Added checks for methods without instance (create)
        # and with multiple instances (list)
        if self.instance is None or len(self.instance) is not 1:
            obj = model()
        else:
            obj = self.instance[0]

        for name in model_field_names:
            if name in self.fields:
                if not obj.has_field_perm(user, field=name, operation='view'):
                    self.fields.remove(name)
                elif not obj.has_field_perm(user, field=name, operation='change'):
                    self.fields[name].read_only = True


class FieldPermissionSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):
    pass
