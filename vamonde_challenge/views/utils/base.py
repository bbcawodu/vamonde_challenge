import sys
import json
from django.http import HttpResponse
from django.db import connection
from django.conf import settings
from .get_parameter_validation_functions import GET_PARAMETER_VALIDATION_FUNCTIONS


class JSONGETRspMixin(object):
    parse_GET_request_and_add_response = None
    accepted_GET_request_parameters = None

    def get(self, request, *args, **kwargs):
        if self.parse_GET_request_and_add_response is None:
            raise NotImplementedError("Need to set class attribute, 'parse_GET_request_and_add_response'.")
        elif self.accepted_GET_request_parameters is None:
            raise NotImplementedError("Need to set class attribute, 'accepted_parameters'. If no parameters are needed, set class attribute to an empty list.")
        else:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, rqst_errors, rqst_warnings = init_response_data()

            # Build dictionary that contains valid Patient Innovation Center GET parameters
            validated_GET_rqst_params = validate_get_request_parameters(request.GET, self.accepted_GET_request_parameters, rqst_errors)

            if not rqst_errors:
                self.parse_GET_request_and_add_response(request, validated_GET_rqst_params, response_raw_data, rqst_errors, rqst_warnings)

            parse_and_log_errors(response_raw_data, rqst_errors, rqst_warnings)
            response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            return response


def validate_get_request_parameters(get_rqst_params, params_to_validate, rqst_errors):
    validated_params = {}

    def run_validation_functions():
        for parameter_to_validate in params_to_validate:
            if parameter_to_validate in GET_PARAMETER_VALIDATION_FUNCTIONS:
                validation_fucntion = GET_PARAMETER_VALIDATION_FUNCTIONS[parameter_to_validate]['function']
                validation_fucntion(get_rqst_params, validated_params, rqst_errors)
            else:
                raise NotImplementedError("GET parameter :{} does not have a validation function implemented.".format(parameter_to_validate))

    run_validation_functions()

    return validated_params


def init_response_data():
    """
    This function returns a skelleton dictionary that can be used for JSON responses

    :return: (type: dictionary) dictionary that can be used in JSON responses
    """
    return {'status': {"error_code": 0, "warnings": [], "version": 1.0, "missing_parameters": [], 'errors': []}, 'data': {}}, [], []


def parse_and_log_errors(response_raw_data, errors_list, rqst_warnings):
    """
    This function takes lists of error and warning messages, adds them to a REST response dictionary, and adds the
    correct error code

    :param response_raw_data: (type: dictionary) dictionary that can be used in REST responses
    :param errors_list: (type: list) list of error messages
    :return: None
    """

    if settings.DEBUG:
        db_statements_made = connection.queries
        print(db_statements_made)
        sys.stdout.flush()

    if errors_list:
        if response_raw_data["status"]["error_code"] == 0:
            response_raw_data["status"]["error_code"] = 1
        response_raw_data["status"]["errors"] = errors_list

        for message in errors_list:
            print(message)
            sys.stdout.flush()

    if rqst_warnings:
        response_raw_data["status"]["warnings"] = rqst_warnings

        for message in errors_list:
            print(message)
            sys.stdout.flush()
