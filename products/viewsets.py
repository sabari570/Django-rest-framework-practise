from rest_framework import mixins, viewsets
from .models import Product
from .serializers import ProductSerializer


# Viewsets are actually same as views but we just have to inherit a viewset and we
# will have all the CRUD endpoints needed for our use GET, POST, PUT, PATCH & DELETE
# out of the box and we can customize them if needed
class ProductViewSet(viewsets.ModelViewSet):
    """
    This will have all the APIs required for a product out of the box
     * get -> list -> Queryset
     * get -> retrieve -> Product Instance Detail View
     * post -> create -> New Instance
     * put -> Update
     * patch -> Partial UPdate
     * delete -> destroy
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"


# Same like this we can also a generic viewset which is quite similar to the generic views we have created
# Where we can actually restrict the apis and also add some mixins to it
# the ListModelMixin and RetrieveModelMixin are provided by the mixins module by rest_framework
# that tells the viewset that thsese are the REST apis we need to use.
class ProductGenericViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    This generic viewset is created only for listing and retrieving a product item:
     * get -> list -> Queryset
     * get -> retrieve -> Product instance detail view
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
