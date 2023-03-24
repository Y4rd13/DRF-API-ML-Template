# Admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission

# Forms
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

### forms.py ###
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser # AbstractBaseUser
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'account_type', 'email', 'phone_number', 'address', 'city', 'state', 'zip_code', 'country', 'is_active', 'is_admin', 'is_staff', 'is_verified', 'is_superuser', 'groups', 'user_permissions', 'last_login',)

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

### admin.py ###
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'username', 'account_type', 'email', 'is_admin', 'is_staff', 'is_verified', 'is_superuser', 'last_login', 'created_at',)
    list_filter = ('id', 'groups', 'is_admin', 'is_staff', 'is_verified', 'is_superuser', 'account_type', 'created_at',)
    fieldsets = (
        (None, {'fields': ('account_type', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'email', 'phone_number', 'address', 'city', 'state', 'zip_code', 'country',)}),
        ('Permissions', {'fields': ("is_admin", "is_staff", "is_superuser", "is_verified", "groups", "user_permissions",)}),
    )

    search_fields = ('id', 'username', 'account_type', 'email', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address', 'city', 'state', 'zip_code', 'country',)
    ordering = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address', 'city', 'state', 'zip_code', 'country',)
    filter_horizontal = ()

    actions = ['delete_selected', 'edit_selected_users', 'remove_selected_permissions']

    def edit_selected_users(self, request, queryset):
        if queryset.count() == 1:
            obj = queryset.first()
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
            return HttpResponseRedirect(url)

        ids = ','.join(str(obj.pk) for obj in queryset)
        url = reverse('admin:%s_%s_changelist' % (obj._meta.app_label, obj._meta.model_name))
        return HttpResponseRedirect("%s?ids=%s" % (url, ids))

    edit_selected_users.short_description = "Edit selected users"

    def save_model(self, request, obj, form, change):
        # Assign all permissions
        obj.save()
        if obj.is_superuser:
            obj.user_permissions.set(Permission.objects.all())
        elif obj.is_admin:
            default_permissions = [
                ('myapp', 'custom user', 'add_customuser'),
                ('myapp', 'custom user', 'change_customuser'),
                ('myapp', 'custom user', 'delete_customuser'),
                ('myapp', 'custom user', 'view_customuser'),
                ('admin', 'log entry', 'view_logentry'),
                ('auth', 'group', 'add_group'),
                ('auth', 'group', 'change_group'),
                ('auth', 'group', 'delete_group'),
                ('auth', 'group', 'view_group'),
                ('auth', 'permission', 'add_permission'),
                ('auth', 'permission', 'change_permission'),
                ('auth', 'permission', 'delete_permission'),
                ('auth', 'permission', 'view_permission'),
                ('authtoken', 'token', 'add_token'),
                ('authtoken', 'token', 'change_token'),
                ('authtoken', 'token', 'delete_token'),
                ('authtoken', 'token', 'view_token'),
                ('contenttypes', 'content type', 'view_contenttype'),
                ('sessions', 'session', 'view_session'),
            ]
            permissions = Permission.objects.filter(content_type__in=default_permissions)
            obj.user_permissions.set(permissions)

        else:
            if obj.id:
                obj.user_permissions.clear()

        super().save_model(request, obj, form, change)

# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
# unregister the Group model from admin.
admin.site.unregister(Group)