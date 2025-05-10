from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import unauthorized_view


from . import views

urlpatterns = [
    path("", views.to_login, name="to_login"),
    path("login", views.custom_login_view, name="login"),
    path('logout', auth_views.LoginView.as_view(), name='logout'),
    path("home", views.home, name="home"),
    path("estimation_period", views.estimation_period, name="estimation_period"),
    path("track_order", views.track_order, name="track_order"),
    path("archive", views.archive, name="archive"),
    path("customers", views.customers, name="customers"),
    path("report", views.report, name="report"),
    path("estimate", views.estimate, name="estimate"),
    path('estimation_schedule/', views.estimation_schedule, name="estimation_schedule/"),
    path("monitor", views.monitor, name="monitor"),
    path("archive", views.archive, name="archive"),
    path("schedule", views.schedule, name="schedule"),
    path("forecasting/exponential_smoothing", views.exponential_smoothing, name="exponential_smoothing"),
    path("forecasting/linear_regression", views.linear_regression, name="linear_regression"),
    path("forecasting/moving_average", views.moving_average, name="moving_average"),
    path("edit/", views.edit, name="edit"),
    path('logout/', views.custom_logout, name='logout'),
    path('unauthorized/', unauthorized_view, name='unauthorized'),
    # path("", views., name=""),
]