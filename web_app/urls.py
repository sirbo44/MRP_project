from django.urls import path

from . import views

urlpatterns = [
    path("", views.to_login, name="to_login"),
    path("login", views.login, name="login")
]