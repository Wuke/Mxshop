from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import mixins
from rest_framework import viewsets

from .filters import GoodsFilter
from .serializers import GoodsSerializer
from goods.models import Goods
from django_filters.rest_framework import DjangoFilterBackend

class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100

class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):

    "list all goods"

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = GoodsFilter

