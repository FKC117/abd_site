from django.urls import path

from .views import home

app_name = "analyticabd"

urlpatterns = [
    path("", home, name="home"),
]
