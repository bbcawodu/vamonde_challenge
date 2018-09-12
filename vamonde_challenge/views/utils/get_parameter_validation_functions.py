import datetime
import re
import urllib
import json


def validate_get_rqst_parameter_from_station_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'from_station_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_starttime(get_rqst_params, validated_params, rqst_errors):
    param_name = 'starttime'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_hh_mm_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_endtime(get_rqst_params, validated_params, rqst_errors):
    param_name = 'endtime'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_hh_mm_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    validated_param_value_list = re.findall("\d+", unvalidated_param_value)
    for indx, element in enumerate(validated_param_value_list):
        validated_param_value_list[indx] = int(element)
    validated_params["{}_{}".format(param_name, "list")] = validated_param_value_list

    if not validated_param_value_list:
        rqst_errors.append('Invalid {}, {}s must be base 10 integers'.format(param_name, param_name))
        return

    number_of_commas = len(re.findall(r",", unvalidated_param_value))
    number_of_parameters_there_should_be = number_of_commas + 1
    if number_of_parameters_there_should_be != len(validated_param_value_list):
        rqst_errors.append(
            'List of {}s is formatted wrong. Values must be base 10 integers separated by commas'.format(param_name))


def validate_yyyy_mm_dd_hh_mm_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    try:
        validated_param_value = datetime.datetime.strptime(unvalidated_param_value, '%Y-%m-%dT%H:%M')
    except ValueError:
        rqst_errors.append('{} parameter value must be a valid datetime formatted like: YYYY-MM-DDTHH:MM. it is: {}'.format(param_name, unvalidated_param_value))
        validated_param_value = None

    validated_params[param_name] = validated_param_value


GET_PARAMETER_VALIDATION_FUNCTIONS = {
    "from_station_id": {
        'function': validate_get_rqst_parameter_from_station_id,
        'type': 'int_with_all'
    },
    "starttime": {
        'function': validate_get_rqst_parameter_starttime,
        'type': 'datetime_string'
    },
    "endtime": {
        'function': validate_get_rqst_parameter_endtime,
        'type': 'datetime_string'
    },
}
