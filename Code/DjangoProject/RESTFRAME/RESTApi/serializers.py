from rest_framework import serializers

from RESTApi.models import UserModel


class UsersSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserModel
        fields = ('url', 'id', 'u_name', 'u_password', 'is_delete', 'is_super')
