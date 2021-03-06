from django.urls import path, include
from . import views
urlpatterns = [
path('latestfilings/',views.latest_filings,name='latest_filings'),
]