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

# Create your views here.
class VendorList(generics.ListCreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    #permission_classes = [permissions.IsAuthenticated]

class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorDetailSerializer
    
class ProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.GET.get('category')
        product_id = self.request.GET.get('id')  # <-- Fix: use 'id' to match your query param
        print(f"category_id: {category_id}, product_id: {product_id}")
        if product_id:
            try:
                return qs.filter(id=product_id)
            except ValueError:
                return qs.none()
        if category_id:
            try:
                category = models.Product_category.objects.get(id=category_id)
                return qs.filter(category=category)
            except models.Product_category.DoesNotExist:
                return qs.none()
        return qs
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer

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
    
class CustomerList(generics.ListCreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    #permission_classes = [permissions.IsAuthenticated]

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerDetailSerializer

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

class OrderDetail(generics.ListAPIView):
    serializer_class = serializers.OrderDetailSerializer

    def get_queryset(self):
        order_id = self.kwargs['pk']
        return models.OrderItem.objects.filter(order_id=order_id)
    
class OrderItemCreate(generics.CreateAPIView):
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderDetailSerializer
    
class CustomerAddressViewSet(viewsets.ModelViewSet):
    queryset = models.CustomerAddress.objects.all()
    serializer_class = serializers.CustomerAddressSerializer
    #permission_classes = [permissions.IsAuthenticated]
    
   
class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = models.ProductRating.objects.all()
    serializer_class = serializers.ProductRatingSerializer
    #permission_classes = [permissions.IsAuthenticated]

class CategoryList(generics.ListCreateAPIView):
    queryset = models.Product_category.objects.all()
    serializer_class = serializers.CategorySerializer
    #permission_classes = [permissions.IsAuthenticated]

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product_category.objects.all()
    serializer_class = serializers.CategoryDetailSerializer

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