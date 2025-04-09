from django.urls import path, re_path

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
    path("estimate", views.estimate, name="estimate"),
    path('estimation_schedule/', views.estimation_schedule, name="estimation_schedule"),
    path("add_order", views.add_order, name="add_order"),
    # path("", views., name=""),
    # path("", views., name=""),
    # path("", views., name=""),
    # path("", views., name=""),
]