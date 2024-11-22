from django.urls import path
from . import views

urlpatterns=[
    # ---------------admin---------------
    path('',views.watch_login),
    path('register',views.register),
    path('watch_home',views.watch_home),
    path('watch_logout',views.watch_shop_logout),
    path('add_product',views.add_product),
    path('edit_product/<pid>',views.edit_product),
    path('delete_product/<pid>',views.delete_product),


    # ---------------user---------------
    path('view_product/<pid>',views.view_product),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path("qty_inc/<cid>",views.qty_inc),
    path("qty_dec/<cid>",views.qty_dec),
    path("remove_cart/<cid>",views.remove_cart),

    
    path('user_home',views.user_home),
    path('contact',views.contact),
    path('booking',views.booking),
    path('about',views.about),
]