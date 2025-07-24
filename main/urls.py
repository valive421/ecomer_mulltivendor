from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'address', views.CustomerAddressViewSet, basename='customer_addresses')
router.register(r'product_ratings', views.ProductRatingViewSet, basename='product_ratings')

urlpatterns = [
 #vendors
 path('vendors/',views.VendorList.as_view()),
 path('vendor/<int:pk>/',views.VendorDetail.as_view()),
 #products
 path('products/',views.ProductList.as_view()),
 path('product/<int:pk>/',views.ProductDetail.as_view()),
 #product categories
 path('categories/',views.CategoryList.as_view()),
 path('category/<int:pk>/',views.CategoryDetail.as_view()),
 #customers 
 path('customers/',views.CustomerList.as_view()),
 path('customer/<int:pk>/',views.CustomerDetail.as_view()),
#orders
 path('orders/',views.OrderList.as_view()),
 path('order/<int:pk>/',views.OrderDetail.as_view()),

    #customer login
    path('customer/login/', views.CustomerLogin, name='customer_login'),
 
]
urlpatterns += router.urls