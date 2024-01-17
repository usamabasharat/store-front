from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product, Collection, Review
from .filters import ProductFilter
from .pagination import DefaultPagination
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer


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
