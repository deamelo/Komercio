from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.permissions import IsSellerOrReadOnly

from .mixins import SerializerByMethodMixin
from .permissions import IsSellerOwnerOrReadOnly
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsSellerOrReadOnly]

    queryset = Product.objects.all()

    serializer_map = {
        "GET": ProductSerializer,
        "POST": ProductDetailSerializer,
    }

    def perform_create(self, serializer):
        if self.request.user.is_seller:
            serializer.save(seller=self.request.user)


class ProductDetailView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOwnerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    serializer_map = {
        "GET": ProductDetailSerializer,
        "PATCH": ProductDetailSerializer,
    }
