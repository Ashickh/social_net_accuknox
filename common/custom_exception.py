import sys
import traceback

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import PermissionDenied,NotFound, MethodNotAllowed
from common.response import failure_response
from common import messages
from django.http import JsonResponse
from rest_framework.settings import api_settings
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first, 
    # to get the standard error response.

    # response = exception_handler(exc, context)

    if isinstance(exc, ObjectDoesNotExist):
        msg = str(exc)


        response = Response(
            {
                 "status": "fail", 
                 "message": msg
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    elif isinstance(exc, ValidationError):
        error_messages = []
        for field, errors in exc.detail.items():
            error_messages.append({
                    'field': field,
                    'message':errors[0],
                })
        msg = error_messages

        response = Response(
            {
                 "status": "fail", 
                 "message": msg
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    elif isinstance(exc, NotAuthenticated):
        print(exc)
        # error_messages = []
        # for field, errors in exc.detail.items():
        #     error_messages.append({
        #             'field': field,
        #             'message':errors[0],
        #         })
        msg = str(exc)

        response = Response(
            {
                 "status": "fail", 
                 "message": msg
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    elif isinstance(exc, PermissionDenied):
        print(exc)
        # error_messages = []
        # for field, errors in exc.detail.items():
        #     error_messages.append({
        #             'field': field,
        #             'message':errors[0],
        #         })
        msg = str(exc)
       
        response = Response(
            {
                 "status": "fail", 
                 "message": msg
            },
            status=status.HTTP_403_FORBIDDEN
        )

    elif isinstance(exc, NotFound):
        print(exc)
        msg = str(exc)
       
        response = Response(
            {
                 "status": "fail", 
                 "message": msg
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    elif isinstance(exc, MethodNotAllowed):
        response = failure_response(status.HTTP_405_METHOD_NOT_ALLOWED, messages.METHOD_NOT_ALLOWED, messages.METHOD_NOT_ALLOWED)
    
    else:
        response = failure_response(status.HTTP_500_INTERNAL_SERVER_ERROR, messages.INTERNAL_SERVER_ERROR, messages.INTERNAL_SERVER_ERROR)

    return response

def error_404(request, exception):
    metadata_class = api_settings.DEFAULT_METADATA_CLASS
    metadata = metadata_class.determine_metadata()
    response = JsonResponse(
            {
                "message": messages.NOT_FOUND, 
                "error" : "Invalid/unknown API route.",
                "data": None,
                "metadata": metadata
            },
            status=status.HTTP_404_NOT_FOUND
        )
    return response
    
      