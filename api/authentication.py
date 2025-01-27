from rest_framework.authentication import TokenAuthentication

# This class is written to customize the token authentication class
# We can manually add any fields if needed like expiresAt inorder to expire the token after certain time
# refer: from rest_framework.authtoken.models.Token class source code
class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
