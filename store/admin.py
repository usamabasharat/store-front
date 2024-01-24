from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import Product, Customer, Collection, ProductImages


class InventoryListFilter(admin.SimpleListFilter):
  title = 'Inventory'
  parameter_name = 'inventory'

  def lookups(self, request, model_admin):
    return [(
        '<10', 'Low'
    )]

  def queryset(self, request, queryset: QuerySet):
    if self.value() == '<10':
      return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):
  model = ProductImages
  readonly_fields = ['thumbnail']

  def thumbnail(self, instance):
    if instance.image.name != '':
      return format_html(f'<img src={instance.image.url} class="thumbnail"/>')
    return ''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  autocomplete_fields = ['collection']
  prepopulated_fields = {'slug': ['title']}
  actions = ['clear_inventory']
  inlines = [ProductImageInline]
  list_display = ['title',
                  'unit_price',
                  'inventory_status',
                  'collection_title']
  list_editable = ['unit_price']
  list_per_page = 10
  list_select_related = ['collection']
  list_filter = ['collection', 'last_update', InventoryListFilter]
  search_fields = ['title__istartswith']

  @admin.display(ordering='inventory')
  def inventory_status(self, product):
    if product.inventory < 10:
      return 'Low'
    return 'Ok'

  @admin.action(description='Clear Inventory')
  def clear_inventory(self, request, queryset):
    updated_count = queryset.update(inventory=0)
    self.message_user(
        request,
        f'{updated_count} products were updated successfully.',
        messages.SUCCESS)

  def collection_title(self, product):
    return product.collection.title

  class Media:
    css = {
        'all': ['store/styles.css']
    }


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['first_name', 'last_name', 'membership']
  list_editable = ['membership']
  list_per_page = 10
  list_select_related = ['user']
  ordering = ['user__first_name', 'user__last_name']
  search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
  list_display = ['title', 'products_count']
  search_fields = ['title']

  @admin.display(ordering='products_count')
  def products_count(self, collection):
    return format_html(
        '<a href="{}">{}</a>',
        reverse('admin:store_product_changelist') + '?' +
        urlencode({'collection__id': str(collection.id)}),
        collection.products_count
    )

  def get_queryset(self, request):
    return super().get_queryset(request).annotate(products_count=Count('products'))
