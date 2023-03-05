# from django.shortcuts import render
# import json
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.hashers import check_password
# from django.shortcuts import render
# from django.utils import timezone
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.exceptions import ValidationError
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.http import HttpResponse
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import generics 
# from buswalaApp.models import sbw_customer
# from buswalaApp.serializers import sbw_customerSerializer,sbw_customerSerializer
# from rest_framework.response import Response

# # Create your views here.
# # Register API
# class RegisterApi(generics.GenericAPIView):
#     serializer_class = sbw_customerSerializer
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         print(request.data)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         user.save()
#         User
#         return Response({
#             # 'Token': access,
#             'email': user.email,
#             "user": sbw_customerSerializer(user, context=self.get_serializer_context()).data,
#             "message": "User Created Successfully.",
#         })
    
# class login(APIView):
#     permission_classes = (AllowAny,)
#     def post(self, request, *args, **kwargs):
#         print(request.data)
#         email = request.data.get("email")
#         print(email)
#         password = request.data.get("password")
#         Account = sbw_customer.objects.get(email=email)
#         serializer = sbw_customerSerializer(Account)
        
#         if email is None or password is None:
#             return Response({'error': 'Please provide both username and password'})
        
#         user = authenticate(email=email, password=password)
#         if not user:
#             return Response({'error': 'Invalid Credentials'})
#         refresh = RefreshToken.for_user(user)
#         print(refresh)
#         login(request, Account)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'message': str(email)+'Login Successful',
            
#         })