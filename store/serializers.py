from decimal import Decimal
from django.db.models import Count
from rest_framework import serializers
from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Collection
    fields = ['id', 'title', 'products_count']

  products_count = serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ['id', 'title', 'description', 'slug',
              'inventory', 'unit_price', 'price_with_tax', 'collection']

  price_with_tax = serializers.SerializerMethodField(
      method_name='calculate_tax')
  collection = serializers.HyperlinkedRelatedField(
      queryset=Collection.objects.all(),
      view_name='collection-detail')

  def calculate_tax(self, product: Product):
    return product.unit_price * Decimal(1.1)
