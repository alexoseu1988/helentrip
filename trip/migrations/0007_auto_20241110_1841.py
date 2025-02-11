# Generated by Django 3.2.13 on 2024-11-10 16:41

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0006_auto_20241109_2140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tour',
            options={'ordering': [django.db.models.expressions.Case(django.db.models.expressions.When(dateStart=None, then=django.db.models.expressions.Value(1)), django.db.models.expressions.When(dateStart__lt=datetime.date(2024, 11, 10), then=django.db.models.expressions.Value(2)), default=django.db.models.expressions.Value(0), output_field=models.IntegerField()), 'dateStart']},
        ),
        migrations.AddField(
            model_name='client',
            name='prepayment',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9, null=True, verbose_name='Розмір передплати'),
        ),
        migrations.AlterField(
            model_name='client',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='trip.payment', verbose_name='Відсоток передплати'),
        ),
    ]
