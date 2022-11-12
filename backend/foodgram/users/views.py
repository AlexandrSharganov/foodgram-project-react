
from api.pagination import CustomPagination
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User, Follow

from .serializers import FollowSerializer, FollowListSerializer


class APIFollow(APIView):
    
    def post(self, request, pk=None):
        user = get_object_or_404(User, username=request.user)
        author = get_object_or_404(User, pk=pk)
        serializer = FollowSerializer(data={"user": user.pk, "author": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        author_serializer = FollowListSerializer(author)
        return Response(
            author_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk=None):
        user = get_object_or_404(User, username=request.user)
        follow = get_object_or_404(Follow, user=user, author=pk)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    pagination_class = CustomPagination
    serializer_class = FollowListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        subscribes = Follow.objects.filter(user=user).values('author')
        return User.objects.filter(pk__in=subscribes)