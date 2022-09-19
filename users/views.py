from rest_framework import generics
from rest_framework.views import APIView, Response, Request, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser

from django.contrib.auth import authenticate

from .permissions import IsOwnerOrReadOnly
from .serializers import LoginSerializer, UserSerializer, UserUpdateIsActiveSerializer, UserFilterOrUpdateOwnerSerializer
from .models import User


class UserView(generics.ListCreateAPIView, PageNumberPagination):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserOrderView(generics.ListAPIView, PageNumberPagination):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
      max_users = self.kwargs["num"]
      return self.queryset.order_by("-date_joined")[0:max_users]


class UserFilterOrUpdateOwnerView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    serializer_class = UserFilterOrUpdateOwnerSerializer
    queryset = User.objects.all()


class UserUpdateIsActiveView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = UserUpdateIsActiveSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "invalid credentials"}, status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})