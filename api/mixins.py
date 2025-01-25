from rest_framework import permissions
from .permissions import IsStaffEditorPermission


# This is a custom mixin that is created for adding a default permission to all the views
# Adding this to a view will add the permission_classes to it, we dont have to manually wrirte them inside the views
class StaffEditorPermissionMixin:
    # Ordering of permissions matter which permission is written first must be satisfied inorder to go to the next
    # Now the permission_classes indicates the permission that the corresponding user has who hit the API
    # If the user has permission to view the products and create them then they can actually do that once authenticated
    # If the user has no permission to view or create a product then he cannot do anything with this API
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]


# Standard Approach =>
# ----------------------
# This is a custom mixin which is created inorder to actually do the filtering of products
# based on which user has hit the request, returns all products if the user is a superuser
# else returns only those products that are created by the user
class UserQuerySetMixin:
    user_field = "user"

    # We redefine the get_queryset function in here such that the view which uses this mixin will automatically
    # place this get_queryset function on its view
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        if user.is_superuser:
            return qs
        return qs.filter(user=user)
