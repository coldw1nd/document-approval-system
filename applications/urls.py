from django.urls import path

from applications import views

app_name = "applications"
urlpatterns = [
    path("", views.index, name="index"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:application_id>/", views.detail, name="detail"),
]
