from rest_framework import routers

from django.urls import include, path

from .views import GroupViewSet, PostViewSet, CommentViewSet, FollowViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='Post')
router.register(r'groups', GroupViewSet, basename='Group')
router.register(r'posts/(?P<id>[0-9]+)/comments',
                CommentViewSet, basename='Comment')
router.register(r'follow', FollowViewSet, basename='Follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
