from django import forms


class FieldPermissionFormMixin:
    """
    ModelForm logic for removing fields when a user is found not to have change permissions.
    """

    def __init__(self, *args, **kwargs):
        super(FieldPermissionFormMixin, self).__init__(*args, **kwargs)

        model = self.Meta.model
        # this might be too broad
        model_field_names = [f.name for f in model._meta.get_fields()]
        for name in model_field_names:
            if name in self.fields and not (self.instance.has_field_perm(self.user, field=name, operation='view') and self.instance.has_field_perm(self.user, field=name, operation='change')):
                self.remove_unauthorized_field(name)

    def remove_unauthorized_field(self, name):
        del self.fields[name]


class FieldPermissionForm(FieldPermissionFormMixin, forms.ModelForm):
    pass
