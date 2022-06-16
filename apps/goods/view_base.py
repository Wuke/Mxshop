import json

from django.views.generic.base import View
from goods.models import Goods

class GoodsListView(View):
    def get(self,request):

        "django view实现商品列表页"

        json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category
        #     json_dict['market_price'] = good.market_price
        #     json_dict['datetime'] = good.add_time
        #     json_list.append(json_dict)

        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        from django.core import serializers
        json_data = serializers.serialize('json',goods)
        json_data = json.loads(json_data)
        from django.http import HttpResponse, JsonResponse
        # json.dumps 出现 serializble issue 用json.dumps(your_data, default=str)
        # return HttpResponse(json.dumps(json_data,default=str),content_type='application/json')
        return JsonResponse(json_data,safe=False)