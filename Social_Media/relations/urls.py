from django.urls import path
from .views import (SearchUserApi,FriendListApi,SendRequest, AcceptRequest, DeleteRequest, PendingRequestList)

urlpatterns = [
    path("search-user/", SearchUserApi.as_view()),
    path("friend-list/", FriendListApi.as_view()),
    path("send-request/", SendRequest.as_view()),
    path("accept-request/", AcceptRequest.as_view()),
    path("delete-request/", DeleteRequest.as_view()),
    path("pending-list/", PendingRequestList.as_view()),

]