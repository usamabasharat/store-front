from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from store.models import Customer
from tags.models import TaggedItem


def say_hello(request):
  TaggedItem.objects.get_tags_for(Customer, 1)

  return render(request, 'hello.html')
