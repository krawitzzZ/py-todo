from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets, status
from rest_framework.decorators import api_view, detail_route, permission_classes
from rest_framework.response import Response

from snippets.models import Snippet, Todo
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, TodoSerializer, UserSerializer


class TodoViewSet(viewsets.ModelViewSet):
  """
    This viewset automatically provides `list`, `create`, `retrieve`,
  `update` and `destroy` actions.
  """
  queryset = Todo.objects.all()
  serializer_class = TodoSerializer

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
  """
  This viewset automatically provides `list` and `detail` actions.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_permissions(self):
    if self.request.method == 'POST':
      return permissions.AllowAny(),
    return permissions.IsAuthenticated(),


class SnippetViewSet(viewsets.ModelViewSet):
  """
  This viewset automatically provides `list`, `create`, `retrieve`,
  `update` and `destroy` actions.

  Additionally we also provide an extra `highlight` action.
  """
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly)

  @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
  def highlight(self, request, *args, **kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
