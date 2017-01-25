from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet, Todo


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
              'date_joined', 'is_active', 'todos', 'snippets',)

  snippets = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                 view_name='snippet-detail')
  todos = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                              view_name='todo-detail')

  # return custom fields by serializer
  # __hidden_fields field is required in serializer
  #
  # def get_fields(self):
  #   fields = super(UserSerializer, self).get_fields()
  #
  #   if self.context.get('view').action != 'create':
  #     for field in self.__hidden_fields:
  #       fields.pop(field, None)
  #   return fields

  def create(self, validated_data):
    user = super(UserSerializer, self).create(validated_data=validated_data)
    user.set_password(validated_data.get('password'))
    print(validated_data.get('password'))
    return user


class TodoSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Todo
    fields = ('url', 'id', 'created', 'updated',
              'owner', 'title', 'description', 'completed',)

  owner = UserSerializer(exclude=('password',))


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Snippet
    fields = ('url', 'id', 'highlight', 'owner',
              'title', 'code', 'linenos', 'language', 'style',)

  owner = serializers.ReadOnlyField(source='owner.username')
  highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight',
                                                   format='html')
