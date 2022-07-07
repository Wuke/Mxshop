import csv
from datetime import datetime

import pandas as pd
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import mixins
from rest_framework import viewsets, permissions
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework_simplejwt import authentication
from django.conf import settings
import import_export

import time

from xadmin.plugins.importexport import ExportMixin
from .filters import GoodsFilter
from .serializers import GoodsSerializer, CategorySerializer, FilterGoodsSerializer
from goods.models import Goods, GoodsCategory
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """商品列表页，分页，搜索，过滤，排序"""
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # GoodsListViewSet认证的演示
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = GoodsPagination
    filter_class = GoodsFilter
    filter_backends = (DjangoFilterBackend,)

    # # 排序
    # ordering_fields = {'shop_price'}
    # # 搜索
    # search_fields = {'name', 'goods_brief'}

    @action(methods=["post"],detail=False)
    def export_filter_location(self, request, *args, **kwargs):
        goods = Goods.objects.filter()
        filter = GoodsFilter(request.GET,queryset=goods).qs
        response = HttpResponse(content_type='text/csv')
        file_name = "fltred_goods_data" + str(datetime.today()) + ".csv"

        writer = csv.writer(response)
        writer.writerow(['category', 'name', 'shop_price'])
        for i in filter.values_list('category', 'name', 'shop_price'):
            writer.writerow(i)
        response['Content-Disposition'] = 'attachment; filename = "' + file_name + '"'
        return response


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """"
    List :
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
