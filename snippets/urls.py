from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from snippets.views import UserViewSet, SnippetViewSet, TodoViewSet

schema_view = get_schema_view(title='TODO API')

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'snippets', SnippetViewSet)
router.register(r'todos', TodoViewSet)

urlpatterns = [
  url('^schema/$', schema_view),
  url(r'^', include(router.urls)),
  url(r'^auth/$', obtain_jwt_token),
  url(r'^auth-token-refresh/$', refresh_jwt_token),
]
