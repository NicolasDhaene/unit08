# Generated by Django 2.2.4 on 2019-08-06 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minerals_catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mineral',
            name='crystal_habit',
            field=models.CharField(max_length=255),
        ),
    ]
