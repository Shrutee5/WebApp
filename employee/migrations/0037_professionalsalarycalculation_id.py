# Generated by Django 4.2.3 on 2023-08-20 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0036_professionalsalarycalculation'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionalsalarycalculation',
            name='id',
            field=models.IntegerField(default=0),
        ),
    ]
