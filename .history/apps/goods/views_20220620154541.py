from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import mixins
from rest_framework import viewsets
from rest_framework import filters
from .filters import GoodsFilter
from .serializers import GoodsSerializer, CategorySerializer
from goods.models import Goods, GoodsCategory
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication

class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100

class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    "商品列表页，分页，搜索，过滤，排序"
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter,)
    # 排序
    ordering_fields = {'shop_price'}
    # 搜索
    search_fields = {'name','goods_brief'}
    filter_class = GoodsFilter

class CategoryViewset(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """"
    List :
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer



