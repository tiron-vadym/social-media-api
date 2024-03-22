from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.views import View
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter

from user.models import User, UserRelation, Post
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    ImageSerializer,
    FollowingSerializer,
    FollowersSerializer,
    PostSerializer,
    PostImageSerializer,
)
from user.permissions import IsOwnerOrReadOnly


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class ManageUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.action == "upload-image":
            return ImageSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/")


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = UserRelation.objects.all().select_related("following")
    serializer_class = FollowingSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowersViewSet(viewsets.ModelViewSet):
    queryset = UserRelation.objects.all().select_related("followers")
    serializer_class = FollowersSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        content = self.request.query_params.get("content")

        if content:
            queryset = queryset.filter(content__icontains=content)

        return queryset.select_related("user")

    def get_serializer_class(self):
        if self.action == "upload-image":
            return PostImageSerializer
        return PostSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        play = self.get_object()
        serializer = self.get_serializer(play, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "content",
                type=str,
                description="content of the post",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of posts."""
        return super().list(request, *args, **kwargs)
