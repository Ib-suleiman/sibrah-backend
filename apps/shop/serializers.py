from rest_framework import serializers
from .models import Product, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductCategory
        fields = ['id', 'name', 'slug', 'icon']

class ProductSerializer(serializers.ModelSerializer):
    category_name    = serializers.CharField(source='category.name', read_only=True)
    in_stock         = serializers.BooleanField(read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    class Meta:
        model  = Product
        fields = ['id','name','slug','category','category_name','description',
                  'price','old_price','discount_percent','icon','badge',
                  'stock','in_stock','is_featured']
