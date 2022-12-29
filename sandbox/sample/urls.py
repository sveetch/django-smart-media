"""
Application URLs
"""
from django.urls import path

from .views import ImageItemDetailView


app_name = "sample"


urlpatterns = [
    path("", BlogIndexView.as_view(), name="index"),
    path("<int:imageitem_pk>/", ImageItemDetailView.as_view(), name="imageitem-detail"),
]
