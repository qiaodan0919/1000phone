from rest_framework import serializers

from movie_user.models import MovieUser


class MovieUserSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=32)
    _password = serializers.CharField(max_length=256)
    phone = serializers.CharField(max_length=32)