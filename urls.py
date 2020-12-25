from django.urls import path
from . import views 
urlpatterns=[
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('details',views.details,name='details'),
    path('addtocart',views.addtocart,name='addtocart'),
    path('profile',views.profile,name='profile'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('cart1',views.cart1,name='cart1'),
    path('remove',views.remove,name='remove'),
    path('checkout',views.checkout,name='checkout'),
    path('payment',views.payment,name='payment'),
    path('cardd/<int:id>/<str:products>/<int:x>/',views.cardd,name='cardd'),
    path('order_product',views.order_product,name='order_product'),
    path('search',views.search,name='search'),
    path('cartincrement',views.cartincrement,name='cartincrement'),
    path('cartdecrement',views.cartdecrement,name='cartdecrement'),
    path('edit',views.edit,name='edit'),
    path('editaddress',views.editaddress,name='editaddress'),
    path('view_product',views.view_product,name='view_product'),
    path('cancel',views.cancel,name='cancel'),
    
]