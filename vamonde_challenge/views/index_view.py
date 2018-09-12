"""
Defines view for the home page
"""
from django.http import HttpResponse


# Defines view for the index of the Vamonde Challenge Server
def index(request):
    return HttpResponse("Welcome to the home page of the Vamonde Challenge Server. Make GET request to /avg_trip_duration to query average trip duration for trips in the database.")