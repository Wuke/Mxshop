import django_filters
from goods.models import Goods
from django.db.models import Q


class GoodsFilter(django_filters.rest_framework.FilterSet):
    # price_min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    # price_max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    # shipping_fee = django_filters.BooleanFilter(field_name='ship_free', lookup_expr='isnull')
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    # top_category = django_filters.NumberFilter(method='top_category_filter')

    # def top_category_filter(self,queryset, name, value):
    #     return queryset.filter(Q(category_id=value) | Q(category_parent_category_id=value) | Q(
    #         category_parent_category_category_parent_category_id=value))

    class Meta:
        model= Goods
        fields = ['is_hot']
