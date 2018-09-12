# Average Trip Duration Endpoint Documentation
[Source Code](../../vamonde_challenge/views/avg_trip_duration_view.py)
- This Endpoint returns the average duration for trips in a given time span. It can also filter results by "from_station_id" of Trips as well as return station data for the given "from_station_id"'s.

- To read average trip duration and station data for a given time period, make a GET request to https://vamonde-challenge-solution.herokuapp.com/avg_trip_duration/
- Example request: https://vamonde-challenge-solution.herokuapp.com/avg_trip_duration/?starttime=2013-06-01T00:00&endtime=2013-12-31T23:59&from_station_id=128,162,5,175,28,85
  - Results returned in the response body will be filtered by the parameters given in the query string of the request url.
  - The parameters given in the REQUIRED query string can be divided into 2 categories: "primary" and "secondary"
  
  - "Primary" parameters - BOTH of these parameters are required in every request.
    - "starttime" - Start datetime of timespan for trips to be included in response. (inclusive)
      - Must be given in "YYYY-MM-DDTHH:MM" format
    - "endtime" - End datetime of timespan for trips to be included in response. (inclusive)
      - Must be given in "YYYY-MM-DDTHH:MM" format
      
  - "Secondary" parameters - Any number of these parameters can be added to a request.
    - "from_station_id" corresponds to 'station_id' of 'from_station' for a given trip.
      - Must be an integer
      - Can be multiple values separated by commas.
    

- The response BODY will be a JSON document with the following format:
```
{
  "status": {
    "error_code": Integer,
    "warnings": Array,
    "version": Integer,
    "missing_parameters": Array,
    "errors": Array
  },
  "data": {
    "from_station_data": [
      {
        "station_id": Integer,
        "name": String,
        "geolocation": String
      },
      ...,
      ...
    ],
    "average_trip_duration": String
  }
}
```

- If there are no errors processing the request:
  - "Error Code" will be 0.
  - Object value of the "data" key will be non empty.
- If there are errors processing the request:
  - "Error Code" will be 1.
  - An array of length > 0 will be the value for the "errors" key in the "status" dictionary.
    - Each item in the array is a string corresponding to an error processing the request.
  - Object value of the "Data" key will be empty.
- Any warnings while processing the request will be given as elements of the array given as the value for the status['warnings'] key.

