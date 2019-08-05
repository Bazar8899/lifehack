from django.urls import path
from user.views import ( register_user , user_info, new_user_oauth)

urlpatterns = [
    path('device', register_user, name='register_user'),
    path('user_info', user_info, name='user_info'),
    path('new_user', new_user_oauth, name='new_user'),
]