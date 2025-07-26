from rest_framework import serializers
from . import models

class VendorSerializer(serializers.ModelSerializer):
    mobile = serializers.IntegerField(read_only=True)
    profile_pic = serializers.ImageField(source='ProfilePicture', read_only=True)

    class Meta:
        model = models.Vendor
        fields = ['user', 'address', 'mobile', 'profile_pic', 'id']
    def __init__(self, *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class VendorDetailSerializer(serializers.ModelSerializer):
    mobile = serializers.IntegerField(read_only=True)
    profile_pic = serializers.ImageField(source='ProfilePicture', read_only=True)

    class Meta:
        model = models.Vendor
        fields = ['user', 'address', 'mobile', 'profile_pic','id']
    def __init__(self, *args, **kwargs):
        super(VendorDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class ProductimgSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id', 'product', 'image']

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

class ProductListSerializer(serializers.ModelSerializer):
    product_images = ProductimgSerializer(many=True, read_only=True)
    class Meta:
        model = models.Product
        fields = ['id', 'category', 'vendor', 'title', 'detail', 'price', 'product_images', 'sells', 'listing_time']
    def __init__(self, *args, **kwargs):
        super(ProductListSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


        
class ProductDetailSerializer(serializers.ModelSerializer):
    product_ratings = serializers.StringRelatedField(many=True, read_only=True)
    product_images = ProductimgSerializer(many=True, read_only=True)
    class Meta:
        model = models.Product
        fields = ['id', 'category', 'vendor', 'title', 'detail', 'price', 'product_ratings', 'product_images', 'sells', 'listing_time']
    def __init__(self, *args, **kwargs):
        super(ProductDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id', 'user', 'mobile']
    def __init__(self, *args, **kwargs):
        super(CustomerSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

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

class CustomerAddressSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=models.Customer.objects.all())
    class Meta:
        model = models.CustomerAddress
        fields = ['id', 'customer', 'address', 'default_address']
    def __init__(self, *args, **kwargs):
        super(CustomerAddressSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductRating
        fields = ['id', 'product', 'customer', 'rating', 'reviews', 'add_time']
    def __init__(self, *args, **kwargs):
        super(ProductRatingSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product_category
        fields = ['id', 'title', 'detail']
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product_category
        fields = ['id', 'title', 'detail']
    def __init__(self, *args, **kwargs):
        super(CategoryDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1