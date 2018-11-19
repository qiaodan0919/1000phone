from rest_framework import serializers

from RESTTwo.models import Students


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ('s_name', 's_age')
        # fields = '__all__'

