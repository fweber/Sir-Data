"""
api_views.py

"""

from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest, JsonResponse
import json
from backend import models
from siddata_backend.recommenders import recommender_functions
from siddata_backend.settings import DEBUG
import datetime





