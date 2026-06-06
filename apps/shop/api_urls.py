from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def products_api(request):
    qs = Product.objects.filter(is_active=True)
    cat = request.GET.get('category', '')
    if cat:
        qs = qs.filter(category__slug=cat)
    return Response(ProductSerializer(qs, many=True).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def categories_api(request):
    cats = ProductCategory.objects.all()
    return Response(ProductCategorySerializer(cats, many=True).data)

urlpatterns = [
    path('products/',   products_api,   name='products_api'),
    path('categories/', categories_api, name='categories_api'),
]
