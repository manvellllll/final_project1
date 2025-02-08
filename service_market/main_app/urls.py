from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = "main_app"

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name='login'),
    path("logout", views.logout, name='logout'),
    path('announcement/<int:id>/', views.announcement_detail, name='announcement_detail'),
    path('add_announcement', views.add_announcement, name='add_announcement')
]