# Generated by Django 5.0.1 on 2024-01-17 20:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
