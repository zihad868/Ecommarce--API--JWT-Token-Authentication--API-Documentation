from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView,PlaceOrderView, UpdateOrderView, OrderItemListCreateView, OrderItemRetrieveUpdateDestroyView, ReviewItemListCreateView, ReviewItemRetrieveUpdateDestroyView

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('products-create/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('order-view/', PlaceOrderView.as_view(), name='order-view'),
    path('order-view/<int:pk>/', UpdateOrderView.as_view(), name='order-detail'),
    path('order-item/', OrderItemListCreateView.as_view(), name='order-item-list-create'),
    path('order-item/<int:pk>/', OrderItemRetrieveUpdateDestroyView.as_view(), name='order-item-detail'),
    path('review/', ReviewItemListCreateView.as_view(), name='review-list-create'),
    path('review/<int:pk>/', ReviewItemRetrieveUpdateDestroyView.as_view(), name='review-detail'),
    
]