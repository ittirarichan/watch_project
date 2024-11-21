from django.urls import path
from . import views

urlpatterns=[
    path('',views.watch_login),
    path('register',views.register),
    path('watch_home',views.watch_home),
    path('watch_logout',views.watch_shop_logout),
    path('add_product',views.add_product),
    path('edit_product/<pid>',views.edit_product),
    path('delete_product/<pid>',views.delete_product),
    path('view_product/<pid>',views.view_product),
    path('view_cart',views.view_cart),

    
    path('user_home',views.user_home),
    path('contact',views.contact),
    path('booking',views.booking),
    path('about',views.about),
]