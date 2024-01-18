from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .pagination import DefaultPagination
from .models import Product, Collection, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemsSerializer, AddToCartItemSerializer


class ProductViewSet(ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_class = ProductFilter
  search_fields = ['title', 'description']
  ordering_fields = ['unit_price', 'updated_at']
  pagination_class = DefaultPagination

  def get_serializer_context(self):
    return {'request': self.request}


class CollectionViewSet(ModelViewSet):
  queryset = Collection.objects.annotate(
      products_count=Count('products')).all()
  serializer_class = CollectionSerializer

  def destroy(self, request, *args, **kwargs):
    if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
      return Response({'error': 'This collection has associated product.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
  serializer_class = ReviewSerializer

  def get_queryset(self):
    return Review.objects.filter(product_id=self.kwargs['product_pk'])

  def get_serializer_context(self):
    return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
  queryset = Cart.objects.prefetch_related('items__product').all()
  serializer_class = CartSerializer


class CartItemsViewSet(ModelViewSet):
  def get_serializer_context(self):
    return {'cart_id': self.kwargs['cart_pk']}

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return AddToCartItemSerializer
    return CartItemsSerializer

  serializer_class = CartItemsSerializer

  def get_queryset(self):
    return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
