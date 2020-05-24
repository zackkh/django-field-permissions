"""
API helpers for django-rest-framework.
"""

from rest_framework import serializers
from django.db.models.query import QuerySet


class FieldPermissionSerializerMixin:
    """
    ModelSerializer logic for marking fields as ``read_only=True`` when a user is found not to have
    change permissions.
    """

    def __init__(self, *args, **kwargs):
        super(FieldPermissionSerializerMixin, self).__init__(*args, **kwargs)

        request = self.context.get('request')
        user = request.user if hasattr(request, 'user') else None
        model = self.Meta.model
        model_field_names = [f.name for f in model._meta.get_fields()]  # this might be too broad

        # Methods without instance eg. create
        if self.instance is None:
            obj = model()
        # Methods with multiple instances, eg. list
        elif isinstance(self.instance, QuerySet):
            obj = model()
        # Methods with one instance, eg. retrieve
        else:
            obj = self.instance

        for name in model_field_names:
            if name in self.fields:
                if not obj.has_field_perm(user, field=name, operation='view'):
                    self.fields.pop(name)
                elif not obj.has_field_perm(user, field=name, operation='change'):
                    self.fields[name].read_only = True


class FieldPermissionSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):
    pass
