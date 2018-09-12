# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, IntegrityError, transaction
import os, datetime


def calculate_and_populate_trip_duration(apps, schema_editor):
  # We can't import models directly as they may be a newer
  # versions than this migration expects. We use the historical version.
  Trip = apps.get_model('vamonde_db', 'Trip')
  all_trip_rows = Trip.objects.all()

  for row in all_trip_rows:
    row.trip_duration = (row.end_time-row.start_time).total_seconds()
    row.save()


def delete_trip_duration(apps, schema_editor):
  # We can't import models directly as they may be a newer
  # versions than this migration expects. We use the historical version.
  Trip = apps.get_model('vamonde_db', 'Trip')
  all_trip_rows = Trip.objects.all()

  for row in all_trip_rows:
    row.trip_duration = None
    row.save()


class Migration(migrations.Migration):
  dependencies = [
    ('vamonde_db', '0002_load_initial_data'),
  ]

  operations = [
    # migrations.RunPython(load_data_from_csv_to_db, reverse_code=migrations.RunPython.noop),
    migrations.RunPython(calculate_and_populate_trip_duration, reverse_code=delete_trip_duration),
  ]
