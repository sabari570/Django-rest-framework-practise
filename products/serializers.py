from rest_framework import serializers
from .models import Product

# Here we define a serializer for the Product model that actually serializers and provides validation to the data


class ProductSerializer(serializers.ModelSerializer):
    # This field is actually created inorder to serialize a function that is created in our model
    # SerializerMethodField is used to include a custom field in the serialized output that is calculated dynamically.
    # The function associated with this field defines how its value is computed.
    my_discount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'content',
                  'price', 'sale_price', 'my_discount']

    # This function is used to tell the serializer which function to serialize from the Model Product
    # here we actually defined a new field my_discount for the serializer inorder for user understandability
    # DRF requires the method associated with a SerializerMethodField to follow the naming pattern get_<field_name>.
    def get_my_discount(self, obj):
        # this line says if the obj returned from the Product model doesnt have an 'id' field then return None
        if not hasattr(obj, 'id'):
            return None
        # this line says if the obj is not an instance of the Product Model then return None
        if not isinstance(obj, Product):
            return None
        # The obj.get_discount() call likely refers to a method defined in the Product model that calculates the discount for the product.
        return obj.get_discount()
