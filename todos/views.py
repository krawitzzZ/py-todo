from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from todos.models import Todo
from todos.serializers import TodoSerializer, UserSerializer


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

  @list_route()
  def me(self, request, *args, **kwargs):
    serializer = UserSerializer(request.user,
                                context={'request': request},
                                exclude=('password',))
    return Response({'user': serializer.data})
