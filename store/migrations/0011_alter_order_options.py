# Generated by Django 5.0.1 on 2024-01-22 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_alter_customer_options_remove_customer_email_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"permissions": [("cancel__order", "Can cancel order")]},
        ),
    ]