# Generated by Django 4.2.3 on 2023-08-19 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0031_incentive_addpayintparti_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StaffSalary',
            new_name='SalaryStructure',
        ),
    ]
