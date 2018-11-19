from rest_framework import serializers

from app.models import UserModel, AddressModel


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AddressModel
        fields = ('id', 'a_address')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    address_list = AddressSerializer(many=True, read_only=True)
    class Meta:
        model = UserModel
        fields = ('url', 'u_name', 'u_password', 'address_list')


