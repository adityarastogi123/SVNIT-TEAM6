from django.urls import path
from .views import *

urlpatterns=[
    path('filter',dateFilter,name='date'),
    path('history-details',getHistory,name='details'),
    path('add-history',addHistory,name='add')
]