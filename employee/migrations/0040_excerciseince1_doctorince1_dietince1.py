# Generated by Django 4.2.3 on 2023-08-24 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0039_professionalsalarycalculation_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcerciseInce1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_expert_name', models.CharField(default='None', max_length=250)),
                ('total_no_of_allotted_participants', models.PositiveIntegerField(default=0)),
                ('total_no_of_participants', models.PositiveIntegerField(default=0)),
                ('patients_in_red', models.PositiveIntegerField(default=0)),
                ('calling_reds', models.CharField(default='0%', max_length=10)),
                ('incentive_1', models.PositiveIntegerField(default=0)),
                ('amount_1', models.FloatField(default=0.0)),
                ('nps_percent', models.CharField(default='0%', max_length=10)),
                ('incentive_2', models.PositiveIntegerField(default=0)),
                ('amount_2', models.FloatField(default=0.0)),
                ('qrs_percent', models.CharField(default='0%', max_length=10)),
                ('incentive_3', models.PositiveIntegerField(default=0)),
                ('amount_3', models.FloatField(default=0.0)),
                ('total_effort_incentive', models.PositiveIntegerField(default=0)),
                ('total_effort_payout', models.FloatField(default=0.0)),
                ('vip_participants', models.PositiveIntegerField(default=0)),
                ('amount_vip_participant', models.FloatField(default=0.0)),
                ('international_participant_alloted', models.PositiveIntegerField(default=0)),
                ('additional_payment', models.FloatField(default=0.0)),
                ('add_pay_for_international_participant', models.FloatField(default=0.0)),
                ('total_effort_incentive_payout', models.FloatField(default=0.0)),
                ('trp', models.FloatField(default=0.0)),
                ('final_effort_incentive_payout', models.FloatField(default=0.0)),
                ('less_tds', models.FloatField(default=0.0)),
                ('net_payout', models.FloatField(default=0.0)),
                ('month', models.CharField(default='None', max_length=50)),
                ('year', models.PositiveIntegerField(default=0)),
                ('empcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employeedetail')),
            ],
            options={
                'db_table': 'ExcerciseInce1',
            },
        ),
        migrations.CreateModel(
            name='DoctorInce1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(default='None', max_length=250)),
                ('total_no_of_allotted_participants', models.PositiveIntegerField(default=0)),
                ('total_no_of_participants', models.PositiveIntegerField(default=0)),
                ('patients_in_red', models.PositiveIntegerField(default=0)),
                ('calling_reds', models.CharField(default='0%', max_length=10)),
                ('incentive_1', models.PositiveIntegerField(default=0)),
                ('amount_1', models.FloatField(default=0.0)),
                ('nps_percent', models.CharField(default='0%', max_length=10)),
                ('incentive_2', models.PositiveIntegerField(default=0)),
                ('amount_2', models.FloatField(default=0.0)),
                ('qrs_percent', models.CharField(default='0%', max_length=10)),
                ('incentive_3', models.PositiveIntegerField(default=0)),
                ('amount_3', models.FloatField(default=0.0)),
                ('total_effort_incentive', models.PositiveIntegerField(default=0)),
                ('total_effort_payout', models.FloatField(default=0.0)),
                ('international_participant_alloted', models.PositiveIntegerField(default=0)),
                ('add_pay_for_international_participant', models.FloatField(default=0.0)),
                ('total_effort_incentive_payout', models.FloatField(default=0.0)),
                ('trp', models.FloatField(default=0.0)),
                ('final_effort_incentive_payout', models.FloatField(default=0.0)),
                ('less_tds', models.FloatField(default=0.0)),
                ('net_payout', models.FloatField(default=0.0)),
                ('month', models.CharField(default='None', max_length=250)),
                ('year', models.PositiveIntegerField(default=0)),
                ('empcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employeedetail')),
            ],
            options={
                'db_table': 'DoctorInce1',
            },
        ),
        migrations.CreateModel(
            name='DietInce1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diet_expert_name', models.CharField(default='None', max_length=250)),
                ('total_no_of_allotted_participants', models.PositiveIntegerField(default=0)),
                ('total_no_of_participants', models.PositiveIntegerField(default=0)),
                ('patients_in_red', models.PositiveIntegerField(default=0)),
                ('calling_reds', models.CharField(default='0%', max_length=10)),
                ('incentive_1', models.PositiveIntegerField(default=0)),
                ('amount_1', models.FloatField(default=0.0)),
                ('nps_percent', models.CharField(default='0%', max_length=10)),
                ('incentive_2', models.PositiveIntegerField(default=0)),
                ('amount_2', models.FloatField(default=0.0)),
                ('qrs_percent', models.CharField(default='0%', max_length=10)),
                ('incentive_3', models.PositiveIntegerField(default=0)),
                ('amount_3', models.FloatField(default=0.0)),
                ('total_effort_incentive', models.PositiveIntegerField(default=0)),
                ('total_effort_payout', models.FloatField(default=0.0)),
                ('vip_patients', models.PositiveIntegerField(default=0)),
                ('amount_vip_participant', models.FloatField(default=0.0)),
                ('international_participant_alloted', models.PositiveIntegerField(default=0)),
                ('add_pay_for_international_participant', models.FloatField(default=0.0)),
                ('total_effort_incentive_payout', models.FloatField(default=0.0)),
                ('less_tds', models.FloatField(default=0.0)),
                ('net_payout', models.FloatField(default=0.0)),
                ('month', models.CharField(default='None', max_length=250)),
                ('year', models.PositiveIntegerField(default=0)),
                ('empcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employeedetail')),
            ],
            options={
                'db_table': 'DietInce1',
            },
        ),
    ]
