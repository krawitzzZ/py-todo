from django.contrib.auth.models import User
from rest_framework import serializers

from todos.models import Todo


class UserSerializer(serializers.HyperlinkedModelSerializer):
  def __init__(self, *args, **kwargs):
    exclude_fields = kwargs.pop('exclude', None)
    super(UserSerializer, self).__init__(*args, **kwargs)

    if exclude_fields is not None:
      excluded = set(exclude_fields)
      for field_name in excluded:
        self.fields.pop(field_name, None)

  class Meta:
    model = User
    fields = ('url', 'id', 'username', 'email', 'password',
              'first_name', 'last_name', 'date_joined', 'is_active',)

  def create(self, validated_data):
    user = super(UserSerializer, self).create(validated_data=validated_data)
    user.set_password(validated_data.get('password'))
    user.save()
    return user


class TodoSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Todo
    fields = ('url', 'id', 'created', 'updated',
              'owner', 'title', 'description', 'completed',)

  owner = UserSerializer(read_only=True, exclude=('password', 'todos',), )
