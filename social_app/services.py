
from datetime import timedelta, timezone
from django.utils import timezone
import requests
from social_net_backend.settings import *
from .serializers import *
from .models import *
from common.response import *
from common import messages
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


def oauth_login(username, password):
    url = API_URL + 'o/token/'
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret,          
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        try:
            data = response.json()  # Attempt to get JSON data
        except ValueError:  # Includes simplejson.decoder.JSONDecodeError
            return {'error': 'Invalid JSON response', 'status': response.status_code}
        
        data['status'] = response.status_code
        return data
    except requests.RequestException as e:
        return {'error': str(e), 'status': response.status_code if hasattr(response, 'status_code') else 500}


def login(request):

    ''' For login operation '''
    try:
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            try:
                user = CustomUser.objects.get(email =username, status=1)
            except CustomUser.DoesNotExist:
                return failure_response(status=status.HTTP_401_UNAUTHORIZED, message=messages.INCORRECT_USERNAME_PASSWORD,data=messages.INCORRECT_USERNAME_PASSWORD)
            username =username
            results = oauth_login(username, password)
            if results["status"] == 200:
                user_info = {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email
                        }
                results["user"] = user_info
                return success_response(status=status.HTTP_200_OK, message=messages.LOGIN_SUCCESS, data=results)
            else:
                if 'status' in results:
                    del results['status']
                return failure_response(status=status.HTTP_401_UNAUTHORIZED, message=messages.LOGIN_FAIL, data=messages.LOGIN_FAIL)
    except Exception as e:
        return failure_response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, message= messages.INPUT_VALIDATION_FAILED, data=serializer.errors)


def create_user(request):

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return success_response(status=status.HTTP_201_CREATED, message=messages.USER_CREATION_SUCESS,data=serializer.data)
    return failure_response(status=status.HTTP_400_BAD_REQUEST, message=messages.USER_CREATION_FAIL, data=serializer.errors)


def search_user(request):
        query = request.query_params.get('q', None)
        if not query:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, message=messages.Q_REQUIRED, data=messages.Q_REQUIRED)
        
        if '@' in query:
            # Search by exact email match
            users = CustomUser.objects.filter(email=query)
        else:
            # Search by name containing the query
            users = CustomUser.objects.filter(Q(username__icontains=query))

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_users = paginator.paginate_queryset(users, request)

        serializer = CustomUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)


def list_friends(request):
        user = request.user
        
        # Get all users where the current user has either sent or received a friend request and it has been accepted
        friends = CustomUser.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__status='accepted') |
            Q(received_requests__from_user=user, received_requests__status='accepted')
        ).distinct()

        serializer = CustomUserSerializer(friends, many=True)
        return success_response(status=status.HTTP_200_OK, message=messages.FRIENDS_LIST,data=serializer.data)

def list_pending_friends(request):
        user = request.user
        
        # Get all users where the current user has either sent or received a friend request and it has been accepted
        friends = CustomUser.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__status='pending') |
            Q(received_requests__from_user=user, received_requests__status='pending')
        ).distinct()

        serializer = CustomUserSerializer(friends, many=True)
        return success_response(status=status.HTTP_200_OK, message=messages.FRIENDS_PENDING_LIST,data=serializer.data)



def send_friend_req(request):
        
    to_user_id = request.data.get('to_user_id')
    if not to_user_id:
        return failure_response(status=status.HTTP_400_BAD_REQUEST, message=messages.FIELD_REQUIRED, data=messages.FIELD_REQUIRED)
    to_user = CustomUser.objects.get(id=to_user_id)
    from_user = request.user

    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').exists():
        return failure_response(status=status.HTTP_400_BAD_REQUEST, message=messages.REQUEST_EXISTS, data=messages.REQUEST_EXISTS)

    recent_requests = FriendRequest.objects.filter(
        from_user=from_user,
        created_at__gte=timezone.now() - timedelta(minutes=1)
    ).count()

    if recent_requests >= 3:
        return failure_response(status=status.HTTP_429_TOO_MANY_REQUESTS, message=messages.REQUEST_LIMIT_EXCEEDS, data=messages.REQUEST_LIMIT_EXCEEDS)

    friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    return success_response(status=status.HTTP_201_CREATED, message=messages.FRIEND_REQ_SENT_SUCCESS,data=FriendRequestSerializer(friend_request).data)
    

def accept_friend_req(request):

    request_id = request.data.get('request_id')
    friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)

    if friend_request.status != 'pending':
        return failure_response(status=status.HTTP_400_BAD_REQUEST, message=messages.REQUEST_ALREADY_RESPONDED, data=messages.REQUEST_ALREADY_RESPONDED)
    
    friend_request.status = 'accepted'
    friend_request.save()
    context = {
        "request_id" : request_id,
        "status" : 'accepted'
    }
    return success_response(status=status.HTTP_200_OK, message=messages.REQUEST_ACCEPTED, data=context)

def reject_friend_req(request):
        
        request_id = request.data.get('request_id')
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)

        if friend_request.status != 'pending':
            return failure_response(status=status.HTTP_400_BAD_REQUEST, message=messages.REQUEST_ALREADY_RESPONDED, data=messages.REQUEST_ALREADY_RESPONDED)
        friend_request.status = 'rejected'
        friend_request.save()
        context = {
        "request_id" : request_id,
        "status" : 'rejected'
    }
        return success_response(status=status.HTTP_200_OK, message=messages.REQUEST_REJECTED, data=context)
