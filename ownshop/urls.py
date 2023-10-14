from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name = 'home'),
    path('faishion/',faishion,name = 'faishion'),
    path('electronics/', electronics, name='electronics'),
    path('about/', about, name='about'),
    path('contact_us/', contact_us, name='contact'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration, name='registration'),
    path('checkout/', checkout, name='checkout'),
    path('products/<int:myid>', product_details, name='product_details'),
    path("payment/", payment, name="payment"),
    path("callback/", callback, name="callback"),
    path('tracker/',tracker,name='tracker'),
    path('adminpage/',admin_view,name='adminpage'),
    path('adminpage/contact',admin_contact_view,name='admincontact'),
    path('adminpage/order',admin_orders_view,name='adminorders'),
    path('adminpage/product',admin_products_view,name='adminproducts'),
    path('adminpage/product/<int:myid>', edit_product_details, name='edit_product_details'),
    path('adminpage/product/addproduct', add_product_details, name='add_product_details'),
    path('adminpage/contact/<int:myid>', edit_contact_details, name='edit_contact_details'),
    path('adminpage/contact/addcontact', add_contact_details, name='add_contact_details'),
    path('adminpage/order/addorder', add_order_details, name='add_order_details'),
    path('adminpage/order/<int:myid>', edit_order_details, name='edit_order_details'),


    path('adminpage/user',admin_users_view,name='adminusers'),
    path('adminpage/user/<int:myid>', edit_user_details, name='edit_user_details'),
    path('adminpage/user/adduser', add_user_details, name='add_user_details'),





]