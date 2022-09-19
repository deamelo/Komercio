from rest_framework import permissions
from rest_framework.views import View, Request

from .models import User


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:

        return request.method in permissions.SAFE_METHODS or (request.user.is_seller)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request:Request, view: View, obj: User) -> bool:

        return request.method in permissions.SAFE_METHODS or (request.user.id == obj.pk)
