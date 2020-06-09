# Generated by Django 3.0.7 on 2020-06-09 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0014_auto_20200609_1437'),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Preparar'), ('A', 'Listo'), ('D', 'Entregado')], default='P', max_length=1)),
                ('date', models.DateField(auto_now_add=True)),
                ('paid_status', models.BooleanField(default=False)),
                ('money_received', models.FloatField(default=0)),
                ('total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('quantity', models.IntegerField(default=1)),
                ('combo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Combo')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='combos',
            field=models.ManyToManyField(through='orders.OrderDetail', to='inventory.Combo'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='clients.Customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='orders.OrderDetail', to='inventory.Product'),
        ),
    ]