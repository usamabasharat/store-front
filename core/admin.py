from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.admin import ProductAdmin, ProductImageInline
from store.models import Product
from tags.models import TaggedItem
from core.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
  add_fieldsets = (
      (
          None,
          {
              "classes": ("wide",),
              "fields": ("first_name", "last_name", "username", "email", "password1", "password2"),
          },
      ),
  )


class TaggedInline(GenericTabularInline):
  autocomplete_fields = ['tag']
  model = TaggedItem
  extra = 0


class CustomProductAdmin(ProductAdmin):
  inlines = [TaggedInline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
