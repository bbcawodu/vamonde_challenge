# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, IntegrityError, transaction
from ..utils import open_csv_file_and_convert_data_to_list
import os, datetime, pytz

cur_path = os.path.dirname(__file__)


def save_row_w_atomic_transaction(row):
  try:
    with transaction.atomic():
      row.save()
  except IntegrityError:
    pass



def delete_row_w_atomic_transaction(row):
  with transaction.atomic():
      row.delete()


def populate_station_table_from_csv_list(station_model, csv_list):
  for row in csv_list:
    from_station_id = row[4]
    from_station_name = row[5]
    to_station_id = row[6]
    to_station_name = row[7]

    from_station_row = station_model(station_id=from_station_id, name=from_station_name)
    save_row_w_atomic_transaction(from_station_row)

    to_station_row = station_model(station_id=to_station_id, name=to_station_name)
    save_row_w_atomic_transaction(to_station_row)


def populate_user_table_from_csv_list(user_model):
  user_row = user_model(user_type="Customer")
  save_row_w_atomic_transaction(user_row)


def populate_trip_table_from_csv_list(trip_model, user_model, station_model, csv_list):
  user_row = user_model.objects.all()[0]

  for row in csv_list:
    trip_id =row[0]
    start_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M').replace(tzinfo=pytz.UTC)
    end_time = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M').replace(tzinfo=pytz.UTC)
    bike_id = row[3]
    from_station_id = row[4]
    to_station_id = row[6]

    trip_row = trip_model(
      trip_id=trip_id,
      start_time=start_time,
      end_time=end_time,
      bike_id=bike_id,
      from_station=station_model.objects.get(station_id=from_station_id),
      to_station=station_model.objects.get(station_id=to_station_id),
      user=user_row
    )
    save_row_w_atomic_transaction(trip_row)


def load_data_from_csv_to_db(apps, schema_editor):
  # We can't import models directly as they may be a newer
  # versions than this migration expects. We use the historical version.
  Station = apps.get_model('vamonde_db', 'Station')
  User = apps.get_model('vamonde_db', 'User')
  Trip = apps.get_model('vamonde_db', 'Trip')

  csv_file_name = os.path.join(os.path.dirname(cur_path), 'divvy_vamonde.csv')
  vamonde_csv_list = open_csv_file_and_convert_data_to_list(csv_file_name)
  vamonde_csv_list = vamonde_csv_list[1:]

  populate_station_table_from_csv_list(Station, vamonde_csv_list)
  populate_user_table_from_csv_list(User)
  populate_trip_table_from_csv_list(Trip, User, Station, vamonde_csv_list)


def delete_initial_data_from_db(apps, schema_editor):
  # We can't import models directly as they may be a newer
  # versions than this migration expects. We use the historical version.
  Station = apps.get_model('vamonde_db', 'Station')
  all_station_rows = Station.objects.all()
  User = apps.get_model('vamonde_db', 'User')
  all_user_rows = User.objects.all()
  Trip = apps.get_model('vamonde_db', 'Trip')
  all_trip_rows = Trip.objects.all()

  for row in all_trip_rows:
    delete_row_w_atomic_transaction(row)
  for row in all_user_rows:
    delete_row_w_atomic_transaction(row)
  for row in all_station_rows:
    delete_row_w_atomic_transaction(row)


class Migration(migrations.Migration):
  dependencies = [
    ('vamonde_db', '0001_initial'),
  ]

  operations = [
    # migrations.RunPython(load_data_from_csv_to_db, reverse_code=migrations.RunPython.noop),
    migrations.RunPython(load_data_from_csv_to_db, reverse_code=delete_initial_data_from_db),
  ]
