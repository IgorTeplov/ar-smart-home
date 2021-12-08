from django.urls import path
from receiver.views import Index

app_name='receiver'

urlpatterns = [
    path('', Index.as_view(), name='index'),
]
