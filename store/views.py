from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import isAdminOrReadOnly
from .filters import ProductFilter
from .pagination import DefaultPagination
from .models import Product, Collection, Review, Cart, CartItem, Customer, Order, ProductImages
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemsSerializer, AddToCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, ProductImageSerializer


class ProductViewSet(ModelViewSet):
  queryset = Product.objects.prefetch_related('images').all()
  serializer_class = ProductSerializer
  permission_classes = [isAdminOrReadOnly]
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
  permission_classes = [isAdminOrReadOnly]

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


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
  queryset = Cart.objects.prefetch_related('items__product').all()
  serializer_class = CartSerializer


class CartItemsViewSet(ModelViewSet):
  http_method_names = ['get', 'post', 'patch', 'delete']
  serializer_class = CartItemsSerializer

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return AddToCartItemSerializer
    elif self.request.method == 'PATCH':
      return UpdateCartItemSerializer
    return CartItemsSerializer

  def get_serializer_context(self):
    return {'cart_id': self.kwargs['cart_pk']}

  def get_queryset(self):
    return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


class CustomerViewSet(ModelViewSet):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer
  permission_classes = [IsAdminUser]

  @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
  def me(self, request):
    (customer, created) = Customer.objects.get(user_id=request.user.id)

    if request.method == 'GET':
      serializer = CustomerSerializer(customer)
      return Response(serializer.data)
    elif request.method == 'PUT':
      serializer = CustomerSerializer(customer, data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)


class OrderViewSet(ModelViewSet):
  http_method_names = ['get', 'patch', 'delete', 'head', 'options']

  def get_permissions(self):
    if self.request.method in ['PATCH', 'DELETE']:
      return [IsAdminUser()]
    return [IsAuthenticated()]

  permission_classes = [IsAuthenticated]

  def create(self, request, *args, **kwargs):
    serializer = CreateOrderSerializer(data=request.data, context={
                                       'user_id': self.request.user.id})
    serializer.is_valid(raise_exception=True)
    order = serializer.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data)

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return CreateOrderSerializer
    elif self.request.method == 'PATCH':
      return UpdateOrderSerializer
    return OrderSerializer

  def get_queryset(self):
    user = self.request.user

    if user.is_staff:
      return Order.objects.all()

    (customer_id, created) = Customer.objects.only(
        'id').get(user_id=user.id)
    return Order.objects.filter(customer_id=customer_id)


class ProductImageViewSet(ModelViewSet):
  serializer_class = ProductImageSerializer

  def get_serializer_context(self):
    return {'product_id': self.kwargs['product_pk']}

  def get_queryset(self):
      return ProductImages.objects.filter(product_id=self.kwargs['product_pk'])
