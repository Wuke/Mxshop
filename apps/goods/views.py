from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import mixins
from rest_framework import viewsets
from rest_framework import filters
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

    "商品列表页，分页，搜索，过滤，排序"

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter,)
    # 排序
    ordering_fields = {'shop_price'}
    # 搜索
    search_fields = {'name','goods_brief'}
    filter_class = GoodsFilter

