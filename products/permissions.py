from rest_framework import permissions
from rest_framework.views import View, Request

from .models import Product

class IsSellerOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request:Request, view: View, obj: Product) -> bool:
        return request.method in permissions.SAFE_METHODS or (request.user == obj.seller)