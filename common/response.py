from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings

# Response structure

        
def responce(status,message,data):
    res = {"status":status,"message":message,"data":data}
    return Response(res)

def success_response(status, message, data):
    return Response(
        {
             "status": "success", 
             "error": None,
             "message": message,
             "data": data, 
        },
        status=status
    )

def failure_response(status, message, data):
    return Response(
        {
            "status": "fail", 
            "message": message, 
            "error" : data,
            "data": None,
        },
        status=status
    )

