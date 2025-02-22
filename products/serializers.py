from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validators import validate_title, unique_product_title
from api.serializers import UserPublicSerialzer

# Here we define a serializer for the Product model that actually serializers and provides validation to the data


class ProductSerializer(serializers.ModelSerializer):
    # Suppose we want to include a field called owner which shows some of the details of the owner of that product
    # this is how we achieve it
    # Here we mention the source because it is from the source we actually get the data, that is here it is the user
    owner = UserPublicSerialzer(source="user", read_only=True)
    # This field is actually created inorder to serialize a function that is created in our model
    # SerializerMethodField is used to include a custom field in the serialized output that is calculated dynamically.
    # The function associated with this field defines how its value is computed.
    my_discount = serializers.SerializerMethodField(read_only=True)

    # Suppose we want to add an url to navigate to product detail page by clicking on it
    # We can create a field for it in the serializer and access them
    # One way to create a link field in serializer is this ->
    edit_url = serializers.SerializerMethodField(read_only=True)

    # Second way to create a link field in serializer is ->
    # HyperlinkedIdentityField() takes the view_name it targets and the url params i.e is the lookup_field
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field="pk",
        # lookup_url_kwarg='pkk' -> If the url params is having any other kwargs other than pk then configure it like this ->
    )

    # Other way of adding a custom validation is this
    # This is how we add multiple validators to a field in the serializer before saving it to DB
    title = serializers.CharField(validators=[validate_title, unique_product_title])

    class Meta:
        model = Product
        fields = [
            "id",
            "url",
            "edit_url",
            "title",
            "content",
            "price",
            "sale_price",
            "my_discount",
            "owner",
        ]

    # Customized validation function for serialzier fields
    # if you need to validate the title field of a serializer before saving it to the DB
    # This is the format of the function validate_<field-name-to-validate>(self, value)
    def validate_title(self, value):
        # This is a queryset which is used to fetch the products that matches with the title we provided
        # iexact means it is case insensitive
        qs = Product.objects.filter(title__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(f"{value} is already a product name")
        return value

    # If you need to update any field before saving it to the database while creating or updating a record
    # customize the create or update function in the serializer
    def create(self, validated_data):
        title = validated_data.get("title")
        content = validated_data.get("content")
        if content is None:
            validated_data["content"] = title
        request = self.context.get("request")
        if request is None:
            return None
        validated_data["user"] = request.user
        return super().create(validated_data)

    # Customized update function
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)

        # If existing content is empty then
        if not instance.content:
            # If the saved data didnt have the content in it then we update the content with the title text
            instance.content = instance.title
        instance.save()
        return instance

    # Now define the function that actually decides what value must be returned to the edit_url field
    def get_edit_url(self, obj):
        # this is how you access the request object in a serializer
        request = self.context.get("request")
        if request is None:
            return None
        # The reverse function from rest_framework is used to target the view to which this URL must navigate to on clicking
        # the name given in the start is the same name we give in the urlpatterns list
        # the kwargs indicates the url params of that view, here its pk which targets -> <int:pk>/ in the param
        # the obj.pk substitutes the value of ok with the object value
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)

    # This function is used to tell the serializer which function to serialize from the Model Product
    # here we actually defined a new field my_discount for the serializer inorder for user understandability
    # DRF requires the method associated with a SerializerMethodField to follow the naming pattern get_<field_name>.
    def get_my_discount(self, obj):
        # this line says if the obj returned from the Product model doesnt have an 'id' field then return None
        if not hasattr(obj, "id"):
            return None
        # this line says if the obj is not an instance of the Product Model then return None
        if not isinstance(obj, Product):
            return None
        # The obj.get_discount() call likely refers to a method defined in the Product model that calculates the discount for the product.
        return obj.get_discount()
