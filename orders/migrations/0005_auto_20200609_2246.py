# Generated by Django 3.0.7 on 2020-06-09 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20200609_1437'),
        ('orders', '0004_auto_20200609_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='combo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='combos', to='inventory.Combo'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.Product'),
        ),
    ]
