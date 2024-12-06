from django.urls import path

from users.views import (
    RegisterAPIView, 
    LoginAPIView, 
    DashboardAPIView,
    LogoutAPIView, 
    CheckAuthAPIView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    ListUserAPIView,
    SubscriptionView,
    AddInterestsAPIView,
    SendFriendRequestView,
    RespondToFriendRequestView,
    FriendListView,
)

app_name = 'users'

urlpatterns = [
    path('api/friends/send_request/<int:user_id>/', SendFriendRequestView.as_view()),
    path('api/friends/respond_request/<int:friendship_id>/', RespondToFriendRequestView.as_view()),
    path('api/friends/list/', FriendListView.as_view(), name='friend_list'),
    path('api/add_interests/', AddInterestsAPIView.as_view(),),
    path('api/subscription/<int:user_id>/', SubscriptionView.as_view(),),
    path('api/list_user/', ListUserAPIView.as_view()),
    path('api/token/', CookieTokenObtainPairView.as_view()),
    path('api/token/refresh/', CookieTokenRefreshView.as_view()),
    path('api/check_auth/', CheckAuthAPIView.as_view()),
    path('api/logout/', LogoutAPIView.as_view()),
    path('api/<int:user_id>/', DashboardAPIView.as_view()),
    path('api/auth/', LoginAPIView.as_view()),
    path('api/create_account/', RegisterAPIView.as_view()),
]
