from django.urls import path

from .views import UserList, UserCreation, UserDetails

urlpatterns = [
    path('', UserList.as_view()),
    path('register/', UserCreation.as_view()),
    path('user/details/', UserDetails.as_view()),
]
