from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


@api_view(['GET', 'POST'])
def product_list(request):
  if request.method == 'GET':
    products = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(
        products, many=True, context={'request': request})
    return Response(serializer.data)
  elif request.method == 'POST':
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
  product = get_object_or_404(Product, pk=id)
  if request.method == 'GET':
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = ProductSerializer(
        product, data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'DELETE':
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_detail(request, pk):
  collection = get_object_or_404(Collection, pk=pk)
  serializer = CollectionSerializer(collection)
  return Response(serializer.data)
