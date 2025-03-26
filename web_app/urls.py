from django.urls import path

from . import views

urlpatterns = [
    path("", views.to_login, name="to_login"),
    path("login", views.login, name="login"),
    path("home", views.home, name="home"),
    path("estimation_period", views.estimation_period, name="estimation_period"),
    path("track_order", views.track_order, name="track_order"),
    path("archive", views.archive, name="archive"),
    path("forecasting", views.forecasting, name="forecasting"),
    path("report", views.report, name="report"),
    # path("", views., name=""),
]