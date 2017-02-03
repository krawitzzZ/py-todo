from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from todos.models import Todo
from todos.serializers import TodoSerializer, UserSerializer
from todos.utils import generate_token


class TodoViewSet(viewsets.ModelViewSet):
  queryset = Todo.objects.all()
  serializer_class = TodoSerializer

  def get_queryset(self):
    user = self.request.user
    todos = Todo.objects.filter(owner=user)
    return todos

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_permissions(self):
    if self.request.method == 'POST':
      return permissions.AllowAny(),
    return permissions.IsAuthenticated(),

  def create(self, request, *args, **kwargs):
    serializer = UserSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    created_user = serializer.data
    created_user.pop('password', None)
    user = User.objects.get(pk=created_user['id'])
    token = generate_token(user)
    return Response({'user': created_user, 'token': token},
                    status=status.HTTP_201_CREATED)

  @list_route()
  def me(self, request, *args, **kwargs):
    serializer = UserSerializer(request.user,
                                context={'request': request},
                                exclude=('password',))
    return Response({'user': serializer.data})
