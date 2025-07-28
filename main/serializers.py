from rest_framework import serializers
from . import models

# Serializer for User fields used in Vendor
class VendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# Serializer for Vendor, includes user info and profile picture
class VendorSerializer(serializers.ModelSerializer):
    user = VendorUserSerializer(read_only=True)
    mobile = serializers.IntegerField(read_only=True)
    profile_pic = serializers.ImageField(source='ProfilePicture', read_only=True)

    class Meta:
        model = models.Vendor
        fields = ['user', 'address', 'mobile', 'profile_pic', 'id']
    def __init__(self, *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Detailed serializer for Vendor
class VendorDetailSerializer(serializers.ModelSerializer):
    user = VendorUserSerializer(read_only=True)
    mobile = serializers.IntegerField(read_only=True)
    profile_pic = serializers.ImageField(source='ProfilePicture', read_only=True)

    class Meta:
        model = models.Vendor
        fields = ['user', 'address', 'mobile', 'profile_pic','id']
    def __init__(self, *args, **kwargs):
        super(VendorDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Serializer for ProductImage model
class ProductimgSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id', 'product', 'image']

# Serializer for Customer profile picture
class profilePictureSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.ProfilePicture
        fields = ['id', 'customer', 'image']

    def get_image(self, obj):
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

# Serializer for listing products, includes images and vendor info
class ProductListSerializer(serializers.ModelSerializer):
    product_images = ProductimgSerializer(many=True, read_only=True)
    vendor = VendorSerializer(read_only=True)
    class Meta:
        model = models.Product
        fields = ['id', 'category', 'vendor', 'title', 'detail', 'price', 'product_images', 'sells', 'listing_time']
    def __init__(self, *args, **kwargs):
        super(ProductListSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

    def create(self, validated_data):
        request = self.context.get('request')
        category_id = request.data.get('category') if request else None
        vendor_id = request.data.get('vendor') if request else None
        category = None
        vendor = None
        if category_id:
            try:
                category = models.Product_category.objects.get(id=category_id)
            except models.Product_category.DoesNotExist:
                pass
        if vendor_id:
            try:
                vendor = models.Vendor.objects.get(id=vendor_id)
            except models.Vendor.DoesNotExist:
                pass
        product = models.Product.objects.create(
            category=category,
            vendor=vendor,
            title=validated_data.get('title'),
            detail=validated_data.get('detail'),
            price=validated_data.get('price'),
        )
        # Handle multiple images
        if request:
            images = request.FILES.getlist('images')
            if not images:
                image = request.FILES.get('image')
                if image:
                    models.ProductImage.objects.create(product=product, image=image)
            else:
                for img in images:
                    models.ProductImage.objects.create(product=product, image=img)
        return product

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # Update fields
        for field in ['title', 'detail', 'price']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        # Update category and vendor if provided
        if request:
            category_id = request.data.get('category')
            vendor_id = request.data.get('vendor')
            if category_id:
                try:
                    instance.category = models.Product_category.objects.get(id=category_id)
                except Exception:
                    pass
            if vendor_id:
                try:
                    instance.vendor = models.Vendor.objects.get(id=vendor_id)
                except Exception:
                    pass
        instance.save()
        # Handle images
        if request:
            images = request.FILES.getlist('images')
            image = request.FILES.get('image')
            if images or image:
                models.ProductImage.objects.filter(product=instance).delete()
                if images:
                    for img in images:
                        models.ProductImage.objects.create(product=instance, image=img)
                elif image:
                    models.ProductImage.objects.create(product=instance, image=image)
        return instance



# Serializer for detailed product info, includes ratings and images
class ProductDetailSerializer(serializers.ModelSerializer):
    product_ratings = serializers.SerializerMethodField()
    product_images = ProductimgSerializer(many=True, read_only=True)
    vendor = VendorSerializer(read_only=True)
    class Meta:
        model = models.Product
        fields = ['id', 'category', 'vendor', 'title', 'detail', 'price', 'product_ratings', 'product_images', 'sells', 'listing_time']
    def __init__(self, *args, **kwargs):
        super(ProductDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

    def get_product_ratings(self, obj):
        # Return all ratings with customer info (including profilepic)
        ratings = models.ProductRating.objects.filter(product=obj).select_related('customer', 'customer__user')
        return ProductRatingWithCustomerSerializer(ratings, many=True, context=self.context).data

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # Update fields
        for field in ['title', 'detail', 'price']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        # Update category and vendor if provided
        if request:
            category_id = request.data.get('category')
            vendor_id = request.data.get('vendor')
            if category_id:
                try:
                    instance.category = models.Product_category.objects.get(id=category_id)
                except Exception:
                    pass
            if vendor_id:
                try:
                    instance.vendor = models.Vendor.objects.get(id=vendor_id)
                except Exception:
                    pass
        instance.save()
        # Handle images
        if request:
            images = request.FILES.getlist('images')
            image = request.FILES.get('image')
            if images or image:
                models.ProductImage.objects.filter(product=instance).delete()
                if images:
                    for img in images:
                        models.ProductImage.objects.create(product=instance, image=img)
                elif image:
                    models.ProductImage.objects.create(product=instance, image=image)
        return instance

# Serializer for Customer model
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id', 'user', 'mobile']
    def __init__(self, *args, **kwargs):
        super(CustomerSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Detailed serializer for Customer, includes profile pictures
class CustomerDetailSerializer(serializers.ModelSerializer):
    profilepic = serializers.SerializerMethodField()

    class Meta:
        model = models.Customer
        fields = ['id', 'user', 'mobile', 'profilepic']

    def get_profilepic(self, instance):
        # Use the correct related_name if set, otherwise fallback to ProfilePicture.objects.filter
        from .models import ProfilePicture
        pics = ProfilePicture.objects.filter(customer=instance)
        return profilePictureSerializer(pics, many=True, context=self.context).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['mobile'] = instance.mobile
        return representation

# Serializer for Order model
class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=models.Customer.objects.all())
    class Meta:
        model = models.Order
        fields = ['id','customer', 'ordertime', 'order_status']

    def create(self, validated_data):
        print("OrderSerializer validated_data:", validated_data)
        return super().create(validated_data)
    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Serializer for OrderItem model
class OrderDetailSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=models.Order.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all())
    class Meta:
        model = models.OrderItem
        fields = ['id', 'order', 'product', 'qty', 'price']
    def __init__(self, *args, **kwargs):
        super(OrderDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

    def create(self, validated_data):
        order_item = super().create(validated_data)
        # Increase the product's sells field by qty
        product = order_item.product
        qty = order_item.qty
        if hasattr(product, 'sells'):
            product.sells = (product.sells or 0) + qty
            product.save(update_fields=['sells'])
        return order_item

# Serializer for CustomerAddress model
class CustomerAddressSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=models.Customer.objects.all())
    class Meta:
        model = models.CustomerAddress
        fields = ['id', 'customer', 'address', 'default_address']
    def __init__(self, *args, **kwargs):
        super(CustomerAddressSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Serializer for ProductRating model
class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductRating
        fields = ['id', 'product', 'customer', 'rating', 'reviews', 'add_time']
    def __init__(self, *args, **kwargs):
        super(ProductRatingSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Serializer for Product_category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product_category
        fields = ['id', 'title', 'detail']
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Detailed serializer for Product_category
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product_category
        fields = ['id', 'title', 'detail']
    def __init__(self, *args, **kwargs):
        super(CategoryDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Serializer for ProductRating with nested customer info
class ProductRatingWithCustomerSerializer(serializers.ModelSerializer):
    customer = CustomerDetailSerializer(read_only=True)
    class Meta:
        model = models.ProductRating
        fields = ['id', 'product', 'customer', 'rating', 'reviews', 'add_time']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = 1