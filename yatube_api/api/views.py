from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from django.shortcuts import get_object_or_404
from posts.models import User, Group, Post
from rest_framework import filters, permissions, viewsets, mixins
from rest_framework.throttling import ScopedRateThrottle

from .pagination import PostPagination
from .permissions import CustomPermission


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Отображение групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    throttle_classes = (ScopedRateThrottle, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class PostViewSet(viewsets.ModelViewSet):
    """Отображение постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    throttle_classes = (ScopedRateThrottle, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          CustomPermission)
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Отображение комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          CustomPermission)
    throttle_classes = (ScopedRateThrottle, )

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """Отображение подписок."""
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, CustomPermission)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('user__username', 'following__username')
    throttle_classes = (ScopedRateThrottle, )

    def get_queryset(self):
        follow = get_object_or_404(User, id=self.request.user.pk)
        queryset = follow.follower.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
