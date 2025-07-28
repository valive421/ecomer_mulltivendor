from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# Router for ViewSets (address, product_ratings)
router = DefaultRouter()
router.register(r'address', views.CustomerAddressViewSet, basename='customer_addresses')
router.register(r'product_ratings', views.ProductRatingViewSet, basename='product_ratings')

urlpatterns = [
 # Vendor endpoints
 # List all vendors or create a new vendor
 path('vendors/',views.VendorList.as_view()),
 # Retrieve, update, or delete a vendor
 path('vendor/<int:pk>/',views.VendorDetail.as_view()),
 # Product endpoints
 # List all products or create a new product
 path('products/',views.ProductList.as_view()),
 # Retrieve, update, or delete a product
 path('product/<int:pk>/',views.ProductDetail.as_view()),
 # Add a review to a product
 path('product/<int:pk>/add_review/', views.add_product_review, name='add_product_review'),
 # Product category endpoints
 path('categories/',views.CategoryList.as_view()),
 path('category/<int:pk>/',views.CategoryDetail.as_view()),
 # Customer endpoints
 path('customers/',views.CustomerList.as_view()),
 path('customer/<int:pk>/',views.CustomerDetail.as_view()),
 # Order endpoints
 path('orders/',views.OrderList.as_view()),
 path('order/<int:pk>/',views.OrderDetail.as_view()),
 # Create order item
 path('orderitem/', views.OrderItemCreate.as_view()),
 # Customer login and registration
 path('customer/login/', views.CustomerLogin, name='customer_login'),
 path('customer/register/', views.CustomerRegister, name='customer_register'),
 # Update order status
 path('order-status/<int:order_id>/',views.order_status, name='order_status'),
 # Customer dashboard
 path('customer-dashboard/<int:pk>/', views.CustomerDashboard, name='customer_dashboard'),
 # Vendor login and registration
 path('vendor/login/', views.VendorLogin, name='vendor_login'),
 path('vendor/register/', views.vendorRegister, name='vendor_register'),
 # Delete product image
 path('product-image/<int:image_id>/', views.ProductImageDelete, name='product_image_delete'),
 # List all order items for a vendor
 path('vendor-order/<int:pk>/', views.vendororderList.as_view(), name='vendor_order_list'),
 # List all addresses for a customer
 path('customer-addresses/<int:customer_id>/', views.customer_addresses, name='customer_addresses'),
 # List all order items for a vendor (paginated)
 path('vendor/<int:vendor_id>/orderitems', views.vendor_orderitems, name='vendor_orderitems'),
 # List all unique customers for a vendor
 path('vendor/<int:vendor_id>/customers/', views.vendor_customers, name='vendor_customers'),
 # List all order items for a vendor and customer
 path('vendor/<int:vendor_id>/customer/<int:customer_id>/orders/', views.vendor_customer_orders, name='vendor_customer_orders'),
 # Change password endpoints
 path('customer/change-password/', views.customer_change_password, name='customer_change_password'),
 path('vendor/change-password/', views.vendor_change_password, name='vendor_change_password'),
]
# Include router URLs for ViewSets
urlpatterns += router.urls