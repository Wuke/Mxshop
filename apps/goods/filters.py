import django_filters
from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    price_min = django_filters.NumberFilter(field_name='shop_price',lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='shop_price',lookup_expr='lte')
    shipping_fee = django_filters.BooleanFilter(field_name='ship_free',lookup_expr='isnull')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ['price_min','price_max','shipping_fee','name']
