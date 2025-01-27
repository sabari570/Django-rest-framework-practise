from rest_framework import serializers


# Here we dont user serializers.ModelSerializers because this is a public serialzer that can be used commonly
# inorder to serialize the user data
# And also always remember that serializers.ModelSerializer is used only when we need to customize the create/update functions
# It is in ModelSerialzer we actually require the class Meta
class UserPublicSerialzer(serializers.Serializer):
    # we put read_only to True because otherwise this field will be shown in the post API body to pass them as a data
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)

    # Now suppose we want to include a field that counts that total number of prodcuts the user has created
    # then we can create a new field and then create the get function to get the data for that field
    total_products = serializers.SerializerMethodField(read_only=True)

    # Defining the function to get the total_products data
    def get_total_products(self, obj):
        user = obj
        user_products_count = user.product_set.count()
        return user_products_count
        # Now if you want to serialize the products data obtained then we do the thing written below
        # return UserProductInlineSerializer(
        #     user_products, many=True, context=self.context
        # ).data


class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", lookup_field="pk", read_only=True
    )
    title = serializers.CharField(read_only=True)
