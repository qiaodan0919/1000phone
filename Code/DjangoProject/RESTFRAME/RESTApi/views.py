import uuid

from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from rest_framework import status, exceptions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from RESTApi.auth import UserAuth
from RESTApi.constants import HTTP_ACTION_REGISTER, HTTP_ACTION_LOGIN
from RESTApi.models import UserModel
from RESTApi.permissions import IsSuperUser
from RESTApi.serializers import UsersSerializer
from RESTFRAME.settings import SUPER_USERS


class UsersView(ListCreateAPIView):
    serializer_class = UsersSerializer
    queryset = UserModel.objects.all()

    authentication_classes = (UserAuth,)
    permission_classes = (IsSuperUser,)

    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action')

        if action == HTTP_ACTION_REGISTER:
            return self.create(request, *args, **kwargs)
        elif action == HTTP_ACTION_LOGIN:
            u_name = request.data.get('u_name')
            u_password = request.data.get('u_password')

            try:
                user = UserModel.objects.get(u_name=u_name)
                if user.u_password == u_password:
                    token = uuid.uuid4().hex
                    cache.set(token,user.id)
                    data = {
                        'msg': 'login success',
                        'status': 200,
                        'token': token
                    }
                    return Response(data)
                else:
                    raise exceptions.AuthenticationFailed

            except UserModel.DoesNotExist:
                raise exceptions.NotFound
        else:
            raise exceptions.ValidationError

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = serializer.data
        u_name = data.get('u_name')

        if u_name in SUPER_USERS:
            u_id = data.get('id')
            user = UserModel.objects.get(pk=u_id)
            user.is_super = True
            user.save()
            data.update({'is_super': True})

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserView(RetrieveUpdateDestroyAPIView):
    serializer_class = UsersSerializer
    queryset = UserModel.objects.all()
