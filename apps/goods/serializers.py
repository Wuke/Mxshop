from rest_framework import serializers
from .models import Goods,GoodsCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        # fields = ('name','click_num','market_price','add_time')
        fields = "__all__"

class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Goods
        # fields = ('name','click_num','market_price','add_time')
        fields = "__all__"