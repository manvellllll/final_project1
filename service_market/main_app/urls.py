from django.urls import path

from . import views


app_name = "main_app"

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name='login'),
    path("logout", views.logout, name='logout'),
]