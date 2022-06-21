"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path

import xadmin
from djangoProject.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
# from goods.view_base import GoodsListView
from goods.views import GoodsListViewSet,CategoryViewset
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

# 配置goods的url
router.register(r'goods',GoodsListViewSet,basename='goods_list')
# 配置GoodsCategory的url
router.register(r'categories',CategoryViewset,basename='categories')

goods_list = GoodsListViewSet.as_view({
    'get':'list',
})

urlpatterns = [
    url('admin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),

    #商品列表页
    url(r'^',include(router.urls)),
    url(r'docs/',include_docs_urls(title='mx生鲜')),
    # drf token
    # url(r'^drf_token', views.obtain_auth_token),
    # jwt token
    url(r'^login/', obtain_jwt_token),
    # url(r'api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # url(r'api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),


]
