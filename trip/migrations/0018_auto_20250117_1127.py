# Generated by Django 3.2.13 on 2025-01-17 09:27

import datetime
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0017_auto_20250116_1152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tour',
            options={'ordering': [django.db.models.expressions.Case(django.db.models.expressions.When(dateStart=None, then=django.db.models.expressions.Value(1)), django.db.models.expressions.When(dateStart__lt=datetime.date(2025, 1, 17), then=django.db.models.expressions.Value(2)), default=django.db.models.expressions.Value(0), output_field=models.IntegerField()), 'dateStart']},
        ),
        migrations.AddField(
            model_name='certificate',
            name='phoneFor',
            field=models.CharField(max_length=20, null=True, verbose_name='Номер телефону, для кого сертифікат'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name='Ваш номер телефону'),
        ),
    ]
