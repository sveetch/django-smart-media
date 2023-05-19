from django.urls import path

from .views import ImageItemDetailView, ImageItemFormView


app_name = "sample"


urlpatterns = [
    path("form/", ImageItemFormView.as_view(), name="imageitem-form"),
    path("<int:imageitem_pk>/", ImageItemDetailView.as_view(), name="imageitem-detail"),
]
