from django.contrib import admin


class FieldPermissionAdminMixin:
    """
        ModelAdmin logic for removing fields when a user is found not to have change permissions.
    """

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        for name in fields:
            instance = obj or self.model()
            if name in fields and not instance.has_field_perm(request.user, field=name):
                fields.remove(name)

        return fields


class FieldPermissionAdmin(FieldPermissionAdminMixin, admin.ModelAdmin):
    pass
