import uuid

from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from  rest_framework import viewsets

from RESTEnd.settings import ROOT_USER_NAME
from app.auth import LoginAuthentication
from app.models import UserModel, AddressModel
from app.permission import RequireLoginPermission, ListAllpermission
from app.serializers import UserSerializer, AddressSerializer


class UsersView(ListCreateAPIView):

    serializer_class = UserSerializer

    queryset = UserModel.objects.all()

    authentication_classes = (LoginAuthentication,)
    permission_classes =(ListAllpermission,)

    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action')

        if action == 'login':

            u_name = request.data.get('u_name')
            u_password = request.data.get('u_password')

            try:
                user = UserModel.objects.get(u_name=u_name)

                if user.u_password != u_password:
                    raise exceptions.AuthenticationFailed

                token = uuid.uuid4().hex
                cache.set(token, user.id)
                data = {
                    'msg': 'ok',
                    'status': '200',
                    'token': token
                }

                return Response(data)

            except UserModel.DoesNotExist:
                raise exceptions.NotFound
        elif action == 'register':
            return self.create(request, *args, **kwargs)
        else:
            raise exceptions.NotFound

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        u_name = data.get('u_name')
        if u_name in ROOT_USER_NAME:
            try:
                user = UserModel.objects.get(u_name= u_name)
                user.is_super = True
                user.save()
                data.update({'is_super': True})
            except:
                raise UserModel.DoesNotExist

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserView(RetrieveUpdateAPIView):

    serializer_class = UserSerializer

    queryset = UserModel.objects.all()

    authentication_classes = (LoginAuthentication,)
    permission_classes = (RequireLoginPermission,)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_super:
            if kwargs.get('pk') != str(request.user.id):
                raise exceptions.PermissionDenied

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AddressView(viewsets.ModelViewSet):
    serializer_class = AddressSerializer

    queryset = AddressModel.objects.all()

    authentication_classes = (LoginAuthentication,)
    permission_classes = (RequireLoginPermission,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = request.user
        a_id = serializer.data.get('id')
        address = AddressModel.objects.get(pk=a_id)
        address.a_user = user
        address.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset.filter(a_user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



