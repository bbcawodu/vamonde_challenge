# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('station_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=1000, unique=True, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('trip_id', models.IntegerField(unique=True)),
                ('bike_id', models.IntegerField()),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('trip_duration', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('from_station', models.ForeignKey(blank=True, null=True, related_name='from_trips', on_delete=django.db.models.deletion.SET_NULL, to='vamonde_db.Station')),
                ('to_station', models.ForeignKey(blank=True, null=True, related_name='to_trips', on_delete=django.db.models.deletion.SET_NULL, to='vamonde_db.Station')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=1000, blank=True, null=True)),
                ('user_type', models.CharField(max_length=100, blank=True, null=True, choices=[('Customer', 'Customer'), ('', ''), (None, None)])),
                ('gender', models.CharField(max_length=100, blank=True, null=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('', ''), (None, None)])),
                ('dob', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vamonde_db.User'),
        ),
    ]
