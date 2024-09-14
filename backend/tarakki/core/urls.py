from django.urls import path

from . import  views
urlpatterns = [
    path("",views.home,name="home"),
    path("signin",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path('dash', views.dashboard_home, name='dashboard_home'),
    path('profile/', views.dashboard_profile, name='dashboard_profile'),
    path('settings/', views.dashboard_settings, name='dashboard_settings'),
]