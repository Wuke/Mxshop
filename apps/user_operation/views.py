from django.shortcuts import render
from rest_framework import viewsets, mixins
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from user_operation.models import UserFav
from user_operation.serializer import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

class UserFavViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
    用户收藏功能
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = 'goods_id'
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
