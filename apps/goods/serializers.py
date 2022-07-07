from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        # fields = ('name','click_num','market_price','add_time')
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        # fields = ('name','click_num','market_price','add_time')
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        # fields = ('name','click_num','market_price','add_time')
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ('name','click_num','market_price','add_time')
        fields = "__all__"

class FilterGoodsSerializer(serializers.Serializer):
    is_hot = serializers.BooleanField()
    name = serializers.CharField(max_length=50,required=False,allow_blank=True)