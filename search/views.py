from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer


# Create your views here.
class SearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        # This returns a ProductQuerySet instance, which means when you call the get_queryset()
        # it calls the get_queryset that is defined inside the ProductManager which returns an instance of ProductQuerySet
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get("query")
        results = Product.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
        return results
