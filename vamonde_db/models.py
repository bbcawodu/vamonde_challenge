from django.db import models
from django.core.validators import MinValueValidator


class Station(models.Model):
  """Table for Stations"""

  station_id = models.IntegerField(unique=True)
  name = models.CharField(blank=True, null=True, max_length=1000, unique=True)

  def serialize_data(self):
    serialized_data = {
      'station_id': self.station_id,
      'name': self.name,
    }

    return serialized_data


class User(models.Model):
  """Table for Users"""

  # Constants for use with column validation and django admin values.
  BLANK = ""
  NULL = None

  CUSTOMER = "Customer"
  USER_TYPE_CHOICES = (
    (CUSTOMER, "Customer"),
    (BLANK, ""),
    (NULL, None)
  )

  MALE = "Male"
  FEMALE = "Female"
  TRANSGENDER = "Transgender"
  GENDER_CHOICES = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (TRANSGENDER, "Transgender"),
    (BLANK, ""),
    (NULL, None)
  )
  #

  name = models.CharField(blank=True, null=True, max_length=1000)
  user_type = models.CharField(blank=True, null=True, max_length=100, choices=USER_TYPE_CHOICES)
  gender = models.CharField(blank=True, null=True, max_length=100, choices=GENDER_CHOICES)
  dob = models.DateField(blank=True, null=True)


class Trip(models.Model):
  """
  Table for Trips
  """

  trip_id = models.IntegerField(unique=True)
  bike_id = models.IntegerField()
  start_time = models.DateTimeField(blank=True, null=True)
  end_time = models.DateTimeField(blank=True, null=True)
  trip_duration = models.FloatField(validators=[MinValueValidator(0.0), ], blank=True, null=True)

  from_station = models.ForeignKey(
    'Station',
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
    related_name='from_trips'
  )
  to_station = models.ForeignKey(
    'Station',
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
    related_name='to_trips'
  )

  user = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)
