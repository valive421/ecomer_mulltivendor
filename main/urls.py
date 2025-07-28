from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
# The following line enables /api/address/ for GET (all), POST (create), and /api/address/<id>/ for GET, PATCH, DELETE
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
 path('product/<int:pk>/add_review/', views.add_product_review, name='add_product_review'),
 #product categories
 path('categories/',views.CategoryList.as_view()),
 path('category/<int:pk>/',views.CategoryDetail.as_view()),
 #customers 
 path('customers/',views.CustomerList.as_view()),
 path('customer/<int:pk>/',views.CustomerDetail.as_view()),
#orders
 path('orders/',views.OrderList.as_view()),
 path('order/<int:pk>/',views.OrderDetail.as_view()),
# Add this endpoint for creating order items:
 path('orderitem/', views.OrderItemCreate.as_view()),
#customer login
path('customer/login/', views.CustomerLogin, name='customer_login'),
path('customer/register/', views.CustomerRegister, name='customer_register'),
  path('order-status/<int:order_id>/',views.order_status, name='order_status'),

path('customer-dashboard/<int:pk>/', views.CustomerDashboard, name='customer_dashboard'),
  # Remove the direct ViewSet mapping; use router for ViewSets
  path('vendor/login/', views.VendorLogin, name='vendor_login'),
path('vendor/register/', views.vendorRegister, name='vendor_register'),
 path('product-image/<int:image_id>/', views.ProductImageDelete, name='product_image_delete'),
 path('vendor-order/<int:pk>/', views.vendororderList.as_view(), name='vendor_order_list'),
 path('customer-addresses/<int:customer_id>/', views.customer_addresses, name='customer_addresses'),
 path('vendor/<int:vendor_id>/orderitems', views.vendor_orderitems, name='vendor_orderitems'),
 path('vendor/<int:vendor_id>/customers/', views.vendor_customers, name='vendor_customers'),
 path('vendor/<int:vendor_id>/customer/<int:customer_id>/orders/', views.vendor_customer_orders, name='vendor_customer_orders'),
 path('customer/change-password/', views.customer_change_password, name='customer_change_password'),
 path('vendor/change-password/', views.vendor_change_password, name='vendor_change_password'),
]
urlpatterns += router.urls