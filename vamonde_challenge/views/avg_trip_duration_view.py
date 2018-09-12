from django.views.generic import View
from django.db.models import Avg
from vamonde_challenge.views.utils import JSONGETRspMixin
from vamonde_db.models import Trip, Station


def check_station_data_list_for_requested_data(data_list, list_of_station_ids, rqst_errors, rqst_warnings):
    if not data_list:
        rqst_errors.append("No Stations in db for given station_ids")
        return

    for station_id in list_of_station_ids:
        tuple_of_bools_if_station_id_in_data_list = (instance_data['station_id'] == station_id for instance_data in data_list)
        if not any(tuple_of_bools_if_station_id_in_data_list):
            rqst_warnings.append('row with station_id: {} not found in database'.format(station_id))


def create_serialized_list_from_db_rows(db_rows):
    return_list = []

    for row in db_rows:
        return_list.append(row.serialize_data())

    return return_list


def get_from_station_serialized_data(from_station_id_list, rqst_errors, rqst_warnings):
    from_station_rows = Station.objects.all().filter(
        station_id__in=from_station_id_list
    )
    station_data_list = create_serialized_list_from_db_rows(from_station_rows)
    check_station_data_list_for_requested_data(station_data_list, from_station_id_list, rqst_errors, rqst_warnings)

    return station_data_list


def calculate_avg_trip_duration_str(matching_trips, validated_GET_rqst_params):
    starttime = validated_GET_rqst_params['starttime']
    endtime = validated_GET_rqst_params['endtime']
    matching_trips = matching_trips.filter(end_time__gte=starttime)
    matching_trips = matching_trips.filter(end_time__lte=endtime)
    average_trip_duration = matching_trips.aggregate(Avg('trip_duration'))['trip_duration__avg']
    atd_minutes, atd_seconds = divmod(average_trip_duration, 60)
    atd_hours, atd_minutes = divmod(atd_minutes, 60)
    average_trip_duration_string = "{} seconds".format(int(atd_seconds))
    if atd_minutes:
        average_trip_duration_string = "{} minutes, ".format(int(atd_minutes)) + average_trip_duration_string
    if atd_hours:
        average_trip_duration_string = "{} hours".format(int(atd_hours)) + average_trip_duration_string

    return average_trip_duration_string

class AverageTripDurationView(JSONGETRspMixin, View):
    """
    Defines views that are associated with average trip duration
    """

    def average_trip_duration_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors, rqst_warnings):
        data_dict = {}
        from_station_id_list = None

        if 'starttime' not in validated_GET_rqst_params or 'endtime' not in validated_GET_rqst_params:
            rqst_errors.append('At least both starttime and endtime must be provided as GET querystring parameters.')
            response_raw_data["data"] = data_dict
            return

        matching_trips = Trip.objects.all()
        if 'from_station_id' in validated_GET_rqst_params:
            from_station_id_list = validated_GET_rqst_params['from_station_id_list']
            matching_trips = matching_trips.filter(from_station__station_id__in=from_station_id_list)
            if not matching_trips.count():
                rqst_errors.append('No trips found for given station_id(\'s).')
                response_raw_data["data"] = data_dict
                return

            from_station_data = get_from_station_serialized_data(from_station_id_list, rqst_errors, rqst_warnings)
            if from_station_data:
                data_dict['from_station_data'] = from_station_data

        average_trip_duration_string = calculate_avg_trip_duration_str(matching_trips, validated_GET_rqst_params)
        data_dict['average_trip_duration'] = average_trip_duration_string

        response_raw_data["data"] = data_dict

    accepted_GET_request_parameters = [
        "starttime",
        "endtime",
        "from_station_id"
    ]
    parse_GET_request_and_add_response = average_trip_duration_get_logic
