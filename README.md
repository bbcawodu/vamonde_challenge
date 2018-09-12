# Vamonde Coding Challenge Solution

This repo serves as the solution to the Vamonde challenge listed below:

```
The attached csv files have data for the 2013 calendar year.


1) Import the attached divvy_vamonde.csv file into a database.
2) Create a new column for trip_duration
3) Perform a migration that calculates and persists the trip duration for each trip.
4) Create a REST endpoint that accepts ‘starttime’ and ‘endtime’ parameters and returns the average duration for that time span in the response.

If you have time:

5) Update the endpoint to accept a ‘from_station_id’ parameter that further filters the results by the stations that the trip started from.  Include the id and name of the station in the response.

If you have further time:

6) Import the attached divvy_vamonde.csv into a separate table in the database. Update the endpoint to also return the latitude and longitude along with the id and name in the response.
```

A Live version of the solution can be found at [Vamonde Challenge Solution](https://vamonde-challenge-solution.herokuapp.com/avg_trip_duration). Documentation at [Documentation](docs/endpoints/avg_trip_duration.md)


## Solution Breakdown
* Import the attached divvy_vamonde.csv file into a database.
  * [Load divvy CSV Django Migration](vamonde_db/migrations/0002_load_initial_data.py)
* Create a new column for trip_duration
  * [Create db Tables from Models Migration](vamonde_db/migrations/0001_initial.py)
* Perform a migration that calculates and persists the trip duration for each trip.
  * [Calculate and Populate trip_duration column Migration](vamonde_db/migrations/0003_populate_trip_duration.py)
* Create a REST endpoint that accepts ‘starttime’ and ‘endtime’ parameters and returns the average duration for that time span in the response.
  * [Source Code](vamonde_challenge/views/avg_trip_duration_view.py)
  * [Documentation](docs/endpoints/avg_trip_duration.md)
* Update the endpoint to accept a ‘from_station_id’ parameter that further filters the results by the stations that the trip started from.  Include the id and name of the station in the response.
  * [Source Code](vamonde_challenge/views/avg_trip_duration_view.py)
  * [Documentation](docs/endpoints/avg_trip_duration.md)
* Import the attached divvy_vamonde.csv into a separate table in the database. Update the endpoint to also return the latitude and longitude along with the id and name in the response.
  * [Source Code](vamonde_db/models.py)
  * [Documentation](docs/endpoints/avg_trip_duration.md)
