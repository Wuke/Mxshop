from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import GoodsSerializer
from goods.models import Goods


class GoodsListView(APIView):
    "list all goods"
    def get(self, request, format=None):
        good = Goods.objects.all()[:10]
        good_serializer = GoodsSerializer(good, many=True)
        return Response(good_serializer.data)
