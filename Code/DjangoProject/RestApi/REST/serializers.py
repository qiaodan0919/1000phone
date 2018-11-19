from django.contrib.auth.models import User, Group
from rest_framework import serializers

from REST.models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('url', 'b_name', 'b_price')