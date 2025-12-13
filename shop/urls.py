from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('cart', views.cart_page, name="cart"),
    path('fav', views.fav_page, name="fav"),
    path('favviewpage/', views.favviewpage, name="favviewpage"),
    path('remove_fav/<str:fid>/', views.remove_fav, name="remove_fav"),
    path('remove_cart/<str:cid>/', views.remove_cart, name="remove_cart"),
    path('collections', views.collections, name="collections"),  # ✅ Keep only one
    path('collections/<str:name>/', views.collectionsview, name="collectionsview"),
    path('collections/<str:cname>/<str:pname>/', views.product_details, name="product_details"),
    path('addtocart', views.add_to_cart, name="addtocart"),
    path('search', views.search, name="search"),
    path('get_cart_count/', views.get_cart_count, name="get_cart_count"),
    path('checkout', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders', views.my_orders, name='my_orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
]