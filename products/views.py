from .serializers import ProductSerializer  # relative imports
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from api.mixins import StaffEditorPermissionMixin  # absolute imports


# Remember to add the permission mixin before the generics API view while inheriting in the class else it wont work
class ProductDetailAPIView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    """
    * DetailView actually gets the detail of one single item
    """

    # queryset is actually the query that we write to retrieve the data, here we can write
    # custom queryset by actually overriding the get_queryset() function
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # The authentication class is already provided in the settings of the project by default if we need to add extra authentication then fill the list with that
    # This lookup_field actually looks for that provided field in the db to fetch the data
    # Here it looks for the pk -> primary key in the db and fetches the data
    # If the url params is having any other kwargs other than pk then configure it like this ->
    # lookup_field = 'pk' # -> generates a queryset like Product.objects.get(pk=1)
    # lookup_url_kwarg = 'pkk'


# This view is used to list all the products and also to create a product


class ProductListCreateAPIView(StaffEditorPermissionMixin, generics.ListCreateAPIView):
    """
    * GET - Used to List out all the products created all at once.
    * POST - Used to create a product
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    """
    * This API is used to update a product detail by id
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"


class ProductDeleteAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    """
    * This API is used to delete a product detail by id
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    # Defining a custom destroy function to delete the product and return the deleted data as response
    def destroy(self, request, *args, **kwargs):
        # Getting the Product instance to be deleted
        instance = self.get_object()

        # serializing the instance data before deleting it
        serializer = self.get_serializer(instance)
        serialized_data = serializer.data

        # Performing the deletion
        self.perform_destroy(instance)
        return Response(
            {
                "messsage": "Product deleted successfully",
                "deleted_product": serialized_data,
            },
            status=status.HTTP_200_OK,
        )


# Here we write a ProductMixinView that can be used and inherited in any class inorder to get
# both the GET and POST endpoints working out of the box, this mixins comes with inbuilt serializer due to which
# we dont have to serialize the data
class ProductMixinView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        # It is from kwargs we get the url param pk
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # Customized create function
    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = title
        serializer.save(content=content)
