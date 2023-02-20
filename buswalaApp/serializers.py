from rest_framework import serializers
from .models import sbw_customer,sbw_CustomerManager
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = sbw_customer
        fields = ['name', 'school_name', 'address',
                  'email', 'password', 'phonenumber','unique_business_id','pick_up_location']

    def create(self, validated_data):
        print("Password")
        print(validated_data)
        print(type(validated_data))
        print(validated_data['password'])
        password = validated_data['password']
        pick_up_location = validated_data['pick_up_location']
        user = sbw_customer.objects.create(
            name=validated_data['name'],
            school_name=validated_data['school_name'],
            address=validated_data['address'],
            email=validated_data['email'],
            is_active=True,
            date_joined=timezone.now(),
            last_login=timezone.now(),
            phonenumber=validated_data['phonenumber'],
        )
        user.set_password(password)
        user.save()
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        user.save()
        return user
    
    
class sbw_customerSerializer(serializers.ModelSerializer):
    class Meta:
        model = sbw_customer
        fields = "__all__"