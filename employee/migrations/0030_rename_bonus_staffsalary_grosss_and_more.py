# Generated by Django 4.2.3 on 2023-08-19 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0029_dietincentive'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffsalary',
            old_name='bonus',
            new_name='grossS',
        ),
        migrations.RenameField(
            model_name='staffsalary',
            old_name='professionalTax',
            new_name='specialAll',
        ),
        migrations.AddField(
            model_name='staffsalary',
            name='syear',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
