from django.urls import path
from . import views


urlpatterns = [
    path("accounts/", views.UserView.as_view(), name="user"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("accounts/newest/<int:num>/", views.UserOrderView.as_view()),
    path("accounts/<pk>/", views.UserFilterOrUpdateOwnerView.as_view(), name="user-datail"),
    path("accounts/<pk>/management/", views.UserUpdateIsActiveView.as_view(), name="admin"),
]