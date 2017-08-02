from django.contrib import admin


class FieldPermissionAdminMixin:
    """
        ModelAdmin logic for removing fields when a user is found not to have change permissions.
    """

    def remove_unauthorized_field(self, name):
        del self.fields[name]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        for name in fields:
            if name in fields and not obj.has_field_perm(request.user, field=name):
                self.remove_unauthorized_field(name)

        return fields


class FieldPermissionAdmin(FieldPermissionAdminMixin, admin.ModelAdmin):
    pass
