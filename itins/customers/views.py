# from django.shortcuts import render
# from rest_framework import permissions, status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.generics import RetrieveAPIView
# from .models import User
# from .serializers import UserSerializer, CustomerRegisterSerializer
# from rest_framework.permissions import AllowAny, IsAuthenticated

# class AgentProfileView(RetrieveAPIView):
#     queryset = User.objects.filter(is_agent=True)
#     serializer_class = UserSerializer

# @api_view(['GET', 'PUT', 'PATCH'])
# @permission_classes([IsAuthenticated])
# def current_user(request):
#     if request.method == 'GET':
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)

#     elif request.method in ['PUT', 'PATCH']:
#         partial = request.method == 'PATCH'
#         serializer = UserSerializer(request.user, data=request.data, partial=partial)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserRegistration(APIView):
#     """
#     Create a new user.
#     """
#     permission_classes = [AllowAny]

#     def post(self, request, format=None):
#         serializer = CustomerRegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)