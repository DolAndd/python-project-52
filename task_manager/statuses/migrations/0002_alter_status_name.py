# Generated by Django 5.1.6 on 2025-04-09 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Имя'),
        ),
    ]
