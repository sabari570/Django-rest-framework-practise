from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view()),
    # The lookup_field should be the same as the keyword argument put here, 'pk'
    path('<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view()),
    path('<int:pk>/delete/', views.ProductDeleteAPIView.as_view()),
]
