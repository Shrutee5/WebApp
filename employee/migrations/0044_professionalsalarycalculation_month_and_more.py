# Generated by Django 4.2.3 on 2023-08-25 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0043_attendancesummary_sundays'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionalsalarycalculation',
            name='month',
            field=models.CharField(default='None', max_length=15),
        ),
        migrations.AddField(
            model_name='professionalsalarycalculation',
            name='year',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
