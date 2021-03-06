# Generated by Django 3.0.7 on 2020-06-28 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('easycomb_theme', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('remarks', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(blank=True, max_length=64)),
                ('phone', models.CharField(max_length=64)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='easycomb_theme.Address')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='easycomb_theme.City')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('cost', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_purchased', to='suppliers.Purchase')),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='products',
            field=models.ManyToManyField(through='suppliers.PurchaseDetail', to='inventory.Product'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.Supplier'),
        ),
    ]
