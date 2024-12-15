# Generated by Django 5.1.3 on 2024-12-13 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0011_delete_passenger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=64)),
                ('last_name', models.CharField(blank=True, max_length=64)),
                ('gender', models.CharField(blank=True, choices=[('male', 'MALE'), ('female', 'FEMALE')], max_length=20)),
            ],
        ),
    ]
