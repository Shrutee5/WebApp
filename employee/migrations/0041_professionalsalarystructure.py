# Generated by Django 4.2.3 on 2023-08-24 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0040_excerciseince1_doctorince1_dietince1'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalSalaryStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(default='None', max_length=250)),
                ('app_salary', models.FloatField(default=0.0)),
                ('professional_salary', models.FloatField(default=0.0)),
                ('start_month', models.CharField(default='None', max_length=15)),
                ('start_year', models.PositiveIntegerField(default=0)),
                ('end_month', models.CharField(default='None', max_length=15)),
                ('end_year', models.PositiveIntegerField(default=0)),
                ('empcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employeedetail')),
            ],
            options={
                'db_table': 'ProfessionalSalaryStructure',
            },
        ),
    ]
