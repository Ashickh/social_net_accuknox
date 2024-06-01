from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
# from common.response import *
from .services import *
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        return login(request=request) 
    

class UserCreateView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        return create_user(request=request)
    
class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return search_user(request=request)
        
class FriendListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return list_friends(request=request)
    

class PendingFriendListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return list_pending_friends(request=request)


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return send_friend_req(request=request)
        
class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return accept_friend_req(request=request)
    

class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return reject_friend_req(request=request)
        