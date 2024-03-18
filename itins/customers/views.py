from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from hotels.models import Hotel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken


@api_view(['GET', 'PUT', 'PATCH'])
# This view will be used anytime the user revisits the site, reloads the page
#  or does anything else that causes React to forget its state. React will check if the user has a token stored in the browser
# if a token is found, it will request this view.
def current_user(request):

    if request.method == 'GET':

        """
        Determine the current user by their token, and return their data
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data)

        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)

        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
