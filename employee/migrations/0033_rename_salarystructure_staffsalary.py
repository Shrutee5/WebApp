# Generated by Django 4.2.3 on 2023-08-19 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0032_rename_staffsalary_salarystructure'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SalaryStructure',
            new_name='StaffSalary',
        ),
    ]
