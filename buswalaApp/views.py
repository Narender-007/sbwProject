from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login,logout as dj_logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics 
from buswalaApp.models import sbw_customer,sbw_driver,sbw_review,sbw_bookingOrder
from buswalaApp.serializers import sbw_customerSerializer,sbw_customerSerializer,sbw_driverSerializer,sbw_reviewSerializer,sbw_bookingOrderSerializer
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from random import randint
from django.core.mail import send_mail
from django.conf import settings
import smtplib, ssl
from rest_framework import status


# Create your views here.



# sending otp to registered user
def send_otp_mail(mail,otp):
    send_mail(
        'OTP',
        'Your OTP is {}'.format(otp),
        settings.EMAIL_HOST_USER,
        [mail],
        fail_silently=False,
    )
  
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "schoolbuswala@ticktechsolutions.tech"  # Enter your address
    password = "Pass@123"
    message = """\
    Subject: This is your OTP

    This message is sent from School bus wala OTP."""+str(otp)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, mail, message)
    return True


# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = sbw_customerSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        user_otp = randint(100000, 999999)
        user_email = request.data['email']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data['password'])
        user.otp_mob_mail = user_otp
        user.save()
        send_otp_mail(user_email, user_otp)
       
        return Response({
            # 'Token': access,
            'email': user.email,
            "user": sbw_customerSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.",
        })
from django.contrib.auth import get_user_model, authenticate

class login(APIView):
    permission_classes = (AllowAny,)
    def post(self,request,*args,**kwargs):
        print(request.data)
        email = request.data.get("email")
        print(email)
        password = request.data.get("password")
        Account = sbw_customer.objects.get(name=email)
        serializer = sbw_customerSerializer(Account)
        # write authinticate login
        UserModel = get_user_model()
        print(serializer.data['password'])
        print(password)
        chck =  check_password(password, serializer.data['password'])
        print(chck)
        user = authenticate(request, name=email, password=password)
        print(user)
        if user is not None:
            dj_login(request, user)
            #create token for user
            print(str(RefreshToken.for_user(user).access_token))
            return Response({
                'email': Account.email,
                "user": serializer.data,
                "message": "User Logged In Successfully.",
                "token": str(RefreshToken.for_user(user).access_token),
                "access_token": str(RefreshToken.for_user(user).access_token),

            })
        else:
            return Response({'error': 'Invalid Credentials'})
        
class logout(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        dj_logout(request)
        return Response({'message': 'User Logged Out Successfully.'})
        # if email is None or password is None:
        #     return Response({'error': 'Please provide both username and password'})
        
        # user = authenticate(email=email, password=password)
        # if not user:
        #     return Response({'error': 'Invalid Credentials'})
        # refresh = RefreshToken.for_user(user)
        # print(refresh)
        # login(request, Account)
        # return Response({
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        #     'message': str(email)+'Login Successful',
            
        # })

class otp_verify(APIView):
    permission_classes = (AllowAny,)
    def post(self,request,*args,**kwargs):
        print(request.data)
        email = request.data.get("email")
        print(email)
        otp = request.data.get("otp")
        print(otp)
        Account = sbw_customer.objects.get(email=email)
        serializer = sbw_customerSerializer(Account)
        # write authinticate login
        UserModel = get_user_model()
        # print(serializer.data['password'])
        print(otp)
        print(serializer.data['otp_mob_mail'])
        v = serializer.data['otp_mob_mail']
        if int(otp) == int(v):
            dj_login(request, Account)
            return Response({
                'email': Account.email,
                "user": serializer.data,
                "message": "User Logged In Successfully.",
            })
        else:
            return Response({'error': 'Invalid Credentials'})
        
#register driver details in database
class driver_register(APIView):
    permission_classes = (AllowAny,)
    serializer_class = sbw_driverSerializer
    def post(self,request,*args,**kwargs):
        print(request.data)
        user_otp = randint(100000, 999999)
        user_email = request.data['driver_email']
        serializer = sbw_driverSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # user.set_password(request.data['password'])
            user.otp_mob_mail = user_otp
            user.save()
            # send_otp_mail(user_email, user_otp)

            return Response({
                "message"  : "Driver Created Successfully.",
                "email" : user.driver_email,
                "user": serializer.data,#sbw_driverSerializer(user, context=self.get_serializer_context()).data,
            })
    #retirve the driver details from database using serializers
    def get(self,request,*args,**kwargs):
        # print(request.data)
        # user_email = request.data['driver_email']
        user = sbw_driver.objects.all()#get(driver_email=user_email)
        serializer = sbw_driverSerializer(user,many=True)
        return Response({
            "message"  : "Driver Details Retrieved Successfully.",
            "user": serializer.data,#sbw_driverSerializer(user, context=self.get_serializer_context()).data,
        })
    #update the driver details in database
    def put(self,request,*args,**kwargs):
        print(request.data)
        user = sbw_driver.objects.get(driver_email=request.data['driver_email'])
        serializer = sbw_driverSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    #delete the driver details from database
    def delete(self,request,*args,**kwargs):
        print(request.data)
        user = sbw_driver.objects.get(driver_email=request.data['driver_email'])
        user.delete()
        return Response({
            "message"  : "Driver Deleted Successfully.",
            "email" : user.driver_email,
            "user": sbw_driverSerializer(user, context=self.get_serializer_context()).data,
        })
    
#create a review in database
class reviews(APIView):
    permission_classes = (AllowAny,)
    serializer_class = sbw_reviewSerializer
    #crate review user 
    def post(self,request,*args,**kwargs):
        print(request.data)
        serializer = sbw_reviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "message"  : "Review Created Successfully.",
                "email" : "serializer.data['driver_email']",
                "review":serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #retrive the review details from database using serializers
    def get(self,request,*args,**kwargs):
        print(request.data)
        # review_id = request.data['review_id']
        # print(review_id)
        Account = sbw_review.objects.all()#(review_id=review_id)
        print(Account)
        serializer = sbw_reviewSerializer(Account, many=True)
        # print(serializer.data)
        return Response(serializer.data)
    #update the review details in database
    def put(self,request,*args,**kwargs):
        print(request.data)
        user = sbw_review.objects.get(review_id=request.data['review_id'])
        serializer = sbw_reviewSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    #delete the review details from database
    def delete(self,request,*args,**kwargs):
        print(request.data)
        user = sbw_review.objects.get(review_id=request.data['review_id'])
        user.delete()
        return Response({
            "message"  : "Review Deleted Successfully.",
            "review": sbw_reviewSerializer(user, context=self.get_serializer_context()).data,
        })
    

#createt bus driver booking stored in database
class booking_create(APIView):
    permission_classes = (AllowAny,)
    serializer_class = sbw_bookingOrderSerializer
    #create booking user 
    def post(self,request,*args,**kwargs):
        print(request.data)
        booking_price = request.data['booking_price']
        booking_mode = request.data['booking_payment_mode']

        serializer = sbw_bookingOrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if booking_mode == "manual":
                user.booking_status = 1
                user.booking_price =  booking_price
                user.save()
                return Response({
                "message"  : "Booking Created Successfully.",
                "payment_status": "manually payment successful",
                
                "booking":serializer.data,
                })
            elif booking_mode == "online":
                user.booking_status = 2
                user.booking_price =  booking_price
                user.save()
                return Response({
                "message"  : "Booking Created Successfully.",
                "payment_status": "online payment successful",
                
                "booking":serializer.data,
                })
            elif booking_mode is None or booking_mode == "":
                user.booking_status = 3

                user.save()
                return Response({
                    "message"  : "Booking Created Successfully.",
                    "payment_status": "Pending",
                    
                    "booking":serializer.data,
                })
            
            return Response({
                "message"  : "Booking Created Successfully.",
                "email" : "serializer.data['driver_email']",
                "booking":serializer.data,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #retrive the booking details from database using serializers
    def get(self,request,*args,**kwargs):
        print(request.data)
        # booking_id = request.data['booking_id']
        # print(booking_id)
        Account = sbw_bookingOrder.objects.all()#(booking_id=booking_id)
        print(Account)
        serializer = sbw_bookingOrderSerializer(Account, many=True)
        # print(serializer.data)
        return Response(serializer.data)
    #update the booking details in database
    def put(self,request,*args,**kwargs):
        print(request.data)
        user = sbw_bookingOrder.objects.get(booking_id=request.data['booking_id'])
        serializer = sbw_bookingOrderSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    #delete the booking details from database
    def delete(self,request,*args,**kwargs):
        print(request.data)
        user = sbw_bookingOrder.objects.get(booking_id=request.data['booking_id'])
        user.delete()
        return Response({
            "message"  : "Booking Deleted Successfully.",
            "booking": sbw_bookingOrderSerializer(user, context=self.get_serializer_context()).data,
        })
    






    
        
    

    
