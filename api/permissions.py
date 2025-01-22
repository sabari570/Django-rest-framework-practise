from rest_framework import permissions


# This is the code which can be used for setting custom permissions for both admin and staff users
# such that we can restrict the access to certain requests based on the user type
# ----------------------------------------------------------------------------------------------------
# class IsStaffEditorPermission(permissions.BasePermission):
#     """
#     Custom permission to only allow admin users to create products.
#     """

#     def has_permission(self, request, view):
#         # Allow all users to perform GET (list products)
#         if request.method == 'GET':
#             return True

#         # Restrict POST method (create product) to admin users (superusers)
#         if request.method == 'POST':
#             # Only allow admin (superuser) to create products
#             return request.user.is_superuser

#         # For other methods (PUT, PATCH, DELETE), restrict to admin users
#         return request.user.is_superuser
# ----------------------------------------------------------------------------------------------------


class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    '''
    This is a custom permission class where we specifically tell whether the user has permission to perform certain actions
    '''
    # Map methods into required permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission codes.
    # So this actually means the user has GET, POST, PUT, PATCH and DELETE access to the product model of the products app
    # If we remove any of the REST API request from here then the user will not be able to access that route, when this custom permission is added to the api view
    perms_map = {
        'GET': ['%(app_label)s.add_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        # This actually means give POST permission to 'products.add_product' => <app_name>.<action>_<model_name>
        'POST': ['%(app_label)s.change_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    # Now the has_permission fn gives permission only to super users and not to staff users
    # def has_permission(self, request, view):
    #     return request.user.is_superuser
