# Generated by Django 5.1.3 on 2024-12-13 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount_credited',
            field=models.DecimalField(decimal_places=2, max_digits=18),
        ),
    ]
