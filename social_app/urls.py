from django.urls import path,include
from social_app import views


urlpatterns = [

    path('login/', views.UserLoginView.as_view()),
    path('create-user/', views.UserCreateView.as_view()),
    path('send-friend-request/', views.SendFriendRequestView.as_view()),
    path('accept-friend-request/', views.AcceptFriendRequestView.as_view()),
    path('reject-friend-request/', views.RejectFriendRequestView.as_view()),
    path('search/', views.UserSearchView.as_view()),
    path('list-friends/', views.FriendListView.as_view()),
    path('pending-list-friends/', views.PendingFriendListView.as_view()),
    
    
    
    
]