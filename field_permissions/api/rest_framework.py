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
        for name in model_field_names:
            if name in self.fields:
                if not self.instance.has_field_perm(user, field=name, operation='view'):
                    self.fields.remove(name)
                    continue
                if not self.instance.has_field_perm(user, field=name, operation='change'):
                    self.fields[name].read_only = True


class FieldPermissionSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):
    pass
