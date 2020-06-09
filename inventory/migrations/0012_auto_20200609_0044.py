# Generated by Django 3.0.7 on 2020-06-09 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_auto_20200609_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='combodetail',
            name='combo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.Combo'),
        ),
        migrations.AlterField(
            model_name='combodetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Product'),
        ),
    ]
