from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import (
    CreateUserView,
    LoginUserView,
    ManageUserView,
    LogoutView,
    FollowingViewSet,
    FollowersViewSet,
    PostViewSet,
)

router = DefaultRouter()
router.register(r"following", FollowingViewSet, basename="following")
router.register(r"followers", FollowersViewSet, basename="followers")
router.register(r"profiles", ManageUserView, basename="profile")
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="token"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include(router.urls)),
]

app_name = "user"
