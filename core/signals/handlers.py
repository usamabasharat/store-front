from django.dispatch import receiver
from store.signals import order_created


@receiver(order_created)
def create_customer_on_new_user(sender, **kwargs):
  print(kwargs['order'])
