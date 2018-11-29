"""blog_vue_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from blog_vue_django.settings import MEDIA_ROOT
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import UserViewSet, SmsCodeViewSet

# 配置goods的url
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name='goods')
router.register(r'category', CategoryViewSet, base_name='category')
router.register(r'codes', SmsCodeViewSet, base_name='codes')
router.register(r'users', UserViewSet, base_name='users')

# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

urlpatterns = [
    path('admin/', admin.site.urls),
    # 商品列表页
    path('', include(router.urls)),

    path('docs/', include_docs_urls(title="blog_vue_django")),
    path('api-auth/', include('rest_framework.urls')),
    # drf自带的token
    path('api-token-auth/', views.obtain_auth_token),
    # jwt认证接口
    path('jwt_auth/', obtain_jwt_token)
]

# 添加静态目录
urlpatterns += static('media/', document_root=MEDIA_ROOT)
