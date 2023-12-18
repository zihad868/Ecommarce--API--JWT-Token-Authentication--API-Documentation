from django.shortcuts import render

from django.db import transaction
from django.db.models.signals import post_save
from rest_framework import viewsets

from .models import Order, Product

from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Order, OrderItem, Review
from api.serializers import RegisterSerializer,LoginSerializer,LogoutSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, ReviewSerializer

# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Product     
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    
# Order 
class PlaceOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        if quantity > product.quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

        order_serializer = self.get_serializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            product.quantity -= quantity
            product.save()
            order_serializer.save()

        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


class UpdateOrderView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_quantity = instance.quantity

        order_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        order_serializer.is_valid(raise_exception=True)

        new_quantity = order_serializer.validated_data.get('quantity')
        product = instance.product

        with transaction.atomic():
            product.quantity += old_quantity  # Add back the old quantity to stock
            if new_quantity > product.quantity:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

            product.quantity -= new_quantity
            product.save()
            order_serializer.save()

        return Response(order_serializer.data)

    
# Order Item
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

class OrderItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    

# Review Items 
class ReviewItemListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class ReviewItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]