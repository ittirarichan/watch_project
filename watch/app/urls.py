from django.urls import path
from . import views

urlpatterns=[
    path('',views.watch_login),
    path('watch_home',views.watch_home),
    path('watch_logout',views.watch_shop_logout),
]