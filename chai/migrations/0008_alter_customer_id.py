# Generated by Django 5.0.6 on 2025-03-29 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chai', '0007_alter_customer_id_order_item_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
