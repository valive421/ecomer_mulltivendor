import profile
from django.shortcuts import render
from . import serializers
from . import models
from rest_framework import generics
from rest_framework import permissions,viewsets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from .serializers import CustomerAddressSerializer
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Product, ProductRating, Customer

from django.views.decorators.csrf import csrf_exempt

# Vendor registration endpoint
@csrf_exempt
def vendorRegister(request):
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    username=request.POST.get('username')
    email=request.POST.get('email')
    mobile=request.POST.get('mobile')
    password=request.POST.get('password')
    address=request.POST.get('address')
    profile_pic=request.FILES.get('profile_pic')
    try:
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        if user:
            try:
                #Create Vendor
                vendor=models.Vendor.objects.create(
                    user=user,
                    mobile=mobile,
                    address=address,
                    ProfilePicture=profile_pic
                )
                msg={
                    'bool':True,
                    'user':user.id,
                    'vendor':vendor.id,
                    'msg':'Successful registration. Procees to Login'
                }
            except IntegrityError:
                msg={
                    'bool':False,
                    'user':'Phone No. already exists!!'
                }
        else:
            msg={
                'bool':False,
                'user':'Something went wrong'
            }
    except IntegrityError:
            msg={
                'bool':False,
                'user':'Username already exists!!'
            }
    return JsonResponse(msg)

# Vendor login endpoint
@csrf_exempt
def VendorLogin(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    if user:
        vendor=models.Vendor.objects.get(user=user)
        msg={
            'bool':True,
            'user':user.username,            
            'id':vendor.id,
        }
        print(msg)
    else:
        msg={
            'bool':False,
            'user':'Invalid Login Credentials'
        }
    return JsonResponse(msg)

# List and create vendors
class VendorList(generics.ListCreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    #permission_classes = [permissions.IsAuthenticated]

# Retrieve, update, or delete a vendor
class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorDetailSerializer
    
# List and create products, supports filtering by category, id, or vendor
class ProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all().order_by('-listing_time')
    serializer_class = serializers.ProductListSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.GET.get('category')
        product_id = self.request.GET.get('id')
        vendor_id = self.request.GET.get('vendor')  # Support vendor filter
        print(f"category_id: {category_id}, product_id: {product_id}, vendor_id: {vendor_id}")
        if product_id:
            try:
                return qs.filter(id=product_id)
            except ValueError:
                return qs.none()
        if vendor_id:
            try:
                return qs.filter(vendor_id=vendor_id)
            except ValueError:
                return qs.none()
        if category_id:
            try:
                return qs.filter(category_id=category_id)
            except ValueError:
                return qs.none()
        return qs

# Retrieve, update, or delete a product
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer
    parser_classes = [MultiPartParser, FormParser]

# Customer registration endpoint
@csrf_exempt
def CustomerRegister(request):
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    username=request.POST.get('username')
    email=request.POST.get('email')
    mobile=request.POST.get('mobile')
    password=request.POST.get('password')
    try:
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        if user:
            try:
                #Create Customer
                customer=models.Customer.objects.create(
                    user=user,
                    mobile=mobile
                )
                msg={
                    'bool':True,
                    'user':user.id,
                    'customer':customer.id,
                    'msg':'Successful registration. Procees to Login'
                }
            except IntegrityError:
                msg={
                    'bool':False,
                    'user':'Phone No. already exists!!'
                }
        else:
            msg={
                'bool':False,
                'user':'Something went wrong'
            }
    except IntegrityError:
            msg={
                'bool':False,
                'user':'Username already exists!!'
            }
    return JsonResponse(msg)

# Customer login endpoint
@csrf_exempt
def CustomerLogin(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    if user:
        customer=models.Customer.objects.get(user=user)
        msg={
            'bool':True,
            'user':user.username,            
            'id':customer.id,
        }
    else:
        msg={
            'bool':False,
            'user':'Invalid Login Credentials'
        }
    return JsonResponse(msg)

# Customer dashboard view, returns order and address counts
def CustomerDashboard(request, pk):
    customer_id = int(pk)
    # Debug: print all orders for this customer
    print(list(models.Order.objects.filter(customer_id=customer_id).values()))
    print("test \n")
    # Check if customer exists
    if not models.Customer.objects.filter(id=customer_id).exists():
        return JsonResponse({'error': 'Customer not found', 'total_orders': 0, 'total_address': 0})

    # Check if any orders exist for this customer
    orders = models.Order.objects.filter(customer_id=customer_id)
    print("Order count for customer", customer_id, ":", orders.count())
    print("Order objects:", list(orders.values()))

    total_orders = orders.count()
    total_address = models.CustomerAddress.objects.filter(customer_id=customer_id).count()
    msg = {
        'total_orders': total_orders,
        'total_address': total_address
    }
    return JsonResponse(msg)
    
# List and create customers
class CustomerList(generics.ListCreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    #permission_classes = [permissions.IsAuthenticated]

# Retrieve, update, or delete a customer, supports profile picture update
class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerDetailSerializer
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()

        # Update user fields if present
        user = instance.user
        user_changed = False
        for field in ['first_name', 'last_name', 'email', 'username']:
            if field in data:
                setattr(user, field, data[field])
                user_changed = True
        if user_changed:
            user.save()

        # Update customer fields
        if 'mobile' in data:
            instance.mobile = data['mobile']
            instance.save()

        # Handle profile picture upload (replace old with new)
        if 'image' in data and data['image']:
            from .models import ProfilePicture
            # Delete all old profile pictures for this customer
            ProfilePicture.objects.filter(customer=instance).delete()
            # Add the new one
            ProfilePicture.objects.create(customer=instance, image=data['image'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

# List and create orders
class OrderList(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Order POST data (raw):", request.data)
        response = super().create(request, *args, **kwargs)
        print("Order create response status:", response.status_code)
        print("Order create response data:", getattr(response, 'data', None))
        return response

# List order items for a specific order
class OrderDetail(generics.ListAPIView):
    serializer_class = serializers.OrderDetailSerializer

    def get_queryset(self):
        order_id = self.kwargs['pk']
        return models.OrderItem.objects.filter(order_id=order_id)
    
# Create an order item
class OrderItemCreate(generics.CreateAPIView):
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderDetailSerializer
    
# ViewSet for customer addresses
class CustomerAddressViewSet(viewsets.ModelViewSet):
    queryset = models.CustomerAddress.objects.all()
    serializer_class = serializers.CustomerAddressSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_id = self.request.query_params.get('customer')
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        return queryset
   
# ViewSet for product ratings
class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = models.ProductRating.objects.all()
    serializer_class = serializers.ProductRatingSerializer
    #permission_classes = [permissions.IsAuthenticated]

# List and create product categories
class CategoryList(generics.ListCreateAPIView):
    queryset = models.Product_category.objects.all()
    serializer_class = serializers.CategorySerializer
    #permission_classes = [permissions.IsAuthenticated]

# Retrieve, update, or delete a product category
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product_category.objects.all()
    serializer_class = serializers.CategoryDetailSerializer

# Update order status (PATCH only)
@csrf_exempt  # Add this decorator to disable CSRF for this view (for testing only)
def order_status(request, order_id):
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = {}
        status = data.get('status')
        updated = models.Order.objects.filter(id=order_id).update(order_status=status)
        msg = {'bool': False}
        if updated:
            msg = {'bool': True}
        return JsonResponse(msg)
    else:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

from django.views.decorators.http import require_http_methods

# Delete a product image by id
@csrf_exempt
@require_http_methods(["DELETE"])
def ProductImageDelete(request, image_id):
    try:
        from .models import ProductImage
        img = ProductImage.objects.get(id=image_id)
        img.delete()
        return JsonResponse({}, status=204)
    except ProductImage.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
    
# List all order items for a vendor
class vendororderList(generics.ListAPIView):
    serializer_class = serializers.OrderDetailSerializer
    queryset = models.OrderItem.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        vendor_id = self.kwargs['pk']
        return qs.filter(product__vendor_id=vendor_id)

# List all addresses for a customer
@csrf_exempt
@require_GET
def customer_addresses(request, customer_id):
    """
    Returns all addresses for a given customer.
    """
    addresses = models.CustomerAddress.objects.filter(customer_id=customer_id)
    serializer = CustomerAddressSerializer(addresses, many=True)
    return JsonResponse(serializer.data, safe=False)

# List all order items for a vendor, paginated, with product and order details
@api_view(['GET'])
def vendor_orderitems(request, vendor_id):
    """
    Returns all order items for a given vendor, with product and order details,
    and includes customer id for each order item.
    """
    qs = models.OrderItem.objects.filter(product__vendor_id=vendor_id).select_related('product', 'order', 'order__customer')
    paginator = PageNumberPagination()
    paginated_qs = paginator.paginate_queryset(qs, request)
    results = []
    for item in paginated_qs:
        # Add customer id if available
        customer_id = None
        if hasattr(item.order, 'customer') and item.order.customer:
            customer_id = item.order.customer.id
        results.append({
            "id": item.id,
            "qty": item.qty,
            "price": item.price,
            "product": {
                "id": item.product.id,
                "title": item.product.title,
                "price": item.product.price,
                "image": item.product.product_images.first().image.url if item.product.product_images.exists() else "",
                "usd_price": getattr(item.product, "usd_price", None),
            },
            "order": {
                "id": item.order.id,
                "order_status": item.order.order_status,
            },
            "customer_id": customer_id
        })
    return paginator.get_paginated_response(results)

# List all unique customers who have ordered from a vendor
@api_view(['GET'])
def vendor_customers(request, vendor_id):
    """
    Returns all unique customers who have ordered products from this vendor.
    """
    # Debug: print vendor_id and type
    # Get all order items for this vendor
    orderitems = models.OrderItem.objects.filter(product__vendor_id=vendor_id).select_related('order', 'order__customer', 'order__customer__user')

    customer_ids = set()
    customers = []
    for item in orderitems:
        order = getattr(item, 'order', None)
        if not order or not hasattr(order, 'customer') or not order.customer:
            continue
        customer = order.customer
        if not hasattr(customer, 'user') or not customer.user:
            continue
        if customer.id not in customer_ids:
            customer_ids.add(customer.id)
            customers.append({
                "customer": {
                    "id": customer.id,
                    "mobile": customer.mobile
                },
                "user": {
                    "id": customer.user.id,
                    "username": customer.user.username,
                    "email": customer.user.email,
                    "first_name": customer.user.first_name,
                    "last_name": customer.user.last_name
                }
            })
    return JsonResponse({"results": customers})

# List all order items for a vendor and a specific customer
@api_view(['GET'])
def vendor_customer_orders(request, vendor_id, customer_id):
    """
    Returns all order items for a given vendor and customer.
    """
    # Get all order items for this vendor and customer
    orderitems = models.OrderItem.objects.filter(
        product__vendor_id=vendor_id,
        order__customer_id=customer_id
    ).select_related('product', 'order')
    results = []
    for item in orderitems:
        results.append({
            "id": item.id,
            "qty": item.qty,
            "price": item.price,
            "product": {
                "id": item.product.id,
                "title": item.product.title,
                "price": item.product.price,
                "image": item.product.product_images.first().image.url if item.product.product_images.exists() else "",
            },
            "order": {
                "id": item.order.id,
                "order_status": item.order.order_status,
            }
        })
    return JsonResponse({"results": results})

# Add a review and rating for a product
@csrf_exempt
@api_view(['POST'])
def add_product_review(request, pk):
    """
    Add a review and rating for a product.
    Expects JSON: { "review": "text", "rating": 1-5 }
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "error": "Product not found."}, status=404)

    data = request.data if hasattr(request, "data") else json.loads(request.body.decode())
    review_text = data.get("review", "").strip()
    rating = int(data.get("rating", 0))

    # You may want to get customer from request.user or session
    # For demo, get customer from request (e.g., pass customer_id in POST)
    customer_id = data.get("customer_id")
    customer = None
    if customer_id:
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found."}, status=404)
    else:
        # Optionally, require authentication and use request.user
        return JsonResponse({"success": False, "error": "Customer ID required."}, status=400)

    if not review_text or not (1 <= rating <= 5):
        return JsonResponse({"success": False, "error": "Review and rating (1-5) required."}, status=400)

    ProductRating.objects.create(
        product=product,
        customer=customer,
        rating=rating,
        reviews=review_text
    )
    return JsonResponse({"success": True})

# Change password for a customer
@csrf_exempt
@api_view(['POST'])
def customer_change_password(request):
    """
    Change password for a customer.
    Expects JSON: { "customer_id": int, "old_password": str, "new_password": str }
    """
    data = request.data if hasattr(request, "data") else json.loads(request.body.decode())
    customer_id = data.get("customer_id")
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    if not (customer_id and old_password and new_password):
        return JsonResponse({"success": False, "error": "All fields required."}, status=400)
    try:
        customer = Customer.objects.get(pk=customer_id)
        user = customer.user
        if not user.check_password(old_password):
            return JsonResponse({"success": False, "error": "Old password is incorrect."}, status=400)
        user.set_password(new_password)
        user.save()
        return JsonResponse({"success": True})
    except Customer.DoesNotExist:
        return JsonResponse({"success": False, "error": "Customer not found."}, status=404)

# Change password for a vendor
@csrf_exempt
@api_view(['POST'])
def vendor_change_password(request):
    """
    Change password for a vendor.
    Expects JSON: { "vendor_id": int, "old_password": str, "new_password": str }
    """
    data = request.data if hasattr(request, "data") else json.loads(request.body.decode())
    vendor_id = data.get("vendor_id")
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    if not (vendor_id and old_password and new_password):
        return JsonResponse({"success": False, "error": "All fields required."}, status=400)
    try:
        vendor = models.Vendor.objects.get(pk=vendor_id)
        user = vendor.user
        if not user.check_password(old_password):
            return JsonResponse({"success": False, "error": "Old password is incorrect."}, status=400)
        user.set_password(new_password)
        user.save()
        return JsonResponse({"success": True})
    except models.Vendor.DoesNotExist:
        return JsonResponse({"success": False, "error": "Vendor not found."}, status=404)