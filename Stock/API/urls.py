from django.urls import path
from .views import *

urlpatterns=[
    path('filter',dateFilter,name='date'),
    path('history-details',getHistory,name='details'),
    path('add-history',addHistory,name='add'),
    path('register',register,name='register'),
    path('login',auth_login,name='login'),
    path('home',home,name='home'),
    path('logout',auth_logout,name='logout')
]