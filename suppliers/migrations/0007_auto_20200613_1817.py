# Generated by Django 3.0.7 on 2020-06-13 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0006_auto_20200611_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='remarks',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='purchasedetail',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
