from .serializers import ProductSerializer  # relative imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from api.mixins import StaffEditorPermissionMixin  # absolute imports

# Remember to add the permission mixin before the generics API view while inheriting in the class else it wont work
class ProductDetailAPIView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    '''
     * DetailView actually gets the detail of one single item
    '''
    # queryset is actually the query that we write to retrieve the data, here we can write
    # custom queryset by actually overriding the get_queryset() function
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # The authentication class is already provided in the settings of the project by default if we need to add extra authentication then fill the list with that
    # This lookup_field actually looks for that provided field in the db to fetch the data
    # Here it looks for the pk -> primary key in the db and fetches the data
    # lookup_field = 'pk' -> generates a queryset like Product.objects.get(pk=1)

# This view is used to list all the products and also to create a product


class ProductListCreateAPIView(StaffEditorPermissionMixin, generics.ListCreateAPIView):
    '''
     * GET - Used to List out all the products created all at once.
     * POST - Used to create a product
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # This is a default function that is used while creation of a product inroder to customize to our needs
    # This function will be executed when we hit a POST request for the given URL else it just lists out all the products created
    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)


class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    '''
     * This API is used to update a product detail by id
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        # The serializer.save() will perform the update using the validated data from the request,
        # and the instance variable will refer to the updated Product object that was just saved to the database.
        instance = serializer.save()
        if not instance.content:
            # If the saved data didnt have the content in it then we update the content with the title text
            instance.content = instance.title


class ProductDeleteAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    '''
     * This API is used to delete a product detail by id
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    # Defining a custom destroy function to delete the product and return the deleted data as response
    def destroy(self, request, *args, **kwargs):
        # Getting the Product instance to be deleted
        instance = self.get_object()

        # serializing the instance data before deleting it
        serializer = self.get_serializer(instance)
        serialized_data = serializer.data

        # Performing the deletion
        self.perform_destroy(instance)
        return Response({
            "messsage": "Product deleted successfully",
            "deleted_product": serialized_data
        }, status=status.HTTP_200_OK)
