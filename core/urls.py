from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.root_redirect, name = 'root'),
    path('home/', views.home, name='home'),
    path ('about/',views.about, name='about'),
    path("api/", include("api.urls")),
    path("", include("users.urls"))
]


