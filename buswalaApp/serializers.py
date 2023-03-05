from rest_framework import serializers
from .models import sbw_customer,sbw_CustomerManager,sbw_driver,sbw_review,sbw_bookingOrder
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import datetime
import uuid


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = sbw_customer
        fields = ['name', 'school_name', 'address',
                  'email', 'password', 'phonenumber','unique_business_id','pick_up_location']

    def create(self, validated_data):
        uuid_id = uuid.uuid4()
        uuid_id_split = str(uuid_id).split('-')[4]
        validated_data['unique_business_id'] = uuid_id_split
        print("Password")
        print(validated_data)
        print(type(validated_data))
        print(validated_data['password'])
        password = make_password(validated_data['password'])
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
            unique_business_id = validated_data['unique_business_id'],
            pick_up_location = pick_up_location,
        )
        user.set_password(password)
        user.save()
        
        return user
    
    
class sbw_customerSerializer(serializers.ModelSerializer):
    class Meta:
        model = sbw_customer
        fields = "__all__"

#create driver serializer
class sbw_driverSerializer(serializers.ModelSerializer):
    class Meta:
        model = sbw_driver
        fields = "__all__"
    # register driver serializer like this fields 'driver_name','bus_no','address','phone_no','email','password','bus_driver_image'
    def create(self, validated_data):
        uuid_id = uuid.uuid4()
        uuid_id_split = str(uuid_id).split('-')[4]
        # validated_data['unique_business_id'] = uuid_id_split
        print("Password")
        print(validated_data)
        print(type(validated_data))
        print(validated_data['password'])
        password = make_password(validated_data['password'])
        # bus_driver_image = validated_data['bus_driver_image']
        user = sbw_driver.objects.create(
            driver_name=validated_data['driver_name'],
            bus_no=validated_data['bus_no'],
            address=validated_data['address'],
            driver_phone_no=validated_data['driver_phone_no'],
            driver_email=validated_data['driver_email'],
            driver_price=validated_data['driver_price'],
            password=password,
            unique_business_id = uuid_id_split
        )
        
        return user
    
#create review serializer
class sbw_reviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = sbw_review
        fields = "__all__"
    
    def create(self, validated_data):
        create_review = sbw_review.objects.create(
            review_title = validated_data['review_title'],
            review_content = validated_data['review_content']   ,
            review_rating = validated_data['review_rating'],
            review_date = validated_data['review_date'],
            review_user = validated_data['review_user'],
            review_driver = validated_data['review_driver'],
        )
        return create_review
    
#create booking order serializer
class sbw_bookingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = sbw_bookingOrder
        fields = "__all__"
    
    def create(self, validated_data):
        import uuid
        uuid_id = uuid.uuid4()
        uuid_id_split = str(uuid_id).split('-')[4]
        # validated_data['unique_business_id'] = uuid_id_split
        
        create_booking_order = sbw_bookingOrder.objects.create(
            booking_driver = validated_data['booking_driver'],
            booking_customer = validated_data['booking_customer'],
            booking_bus_no = validated_data['booking_bus_no'],
            booking_bus_location = validated_data['booking_bus_location'],
            booking_bus_image = validated_data['booking_bus_image'],
            booking_bus_status = validated_data['booking_bus_status'],
            booking_bus_driver_image = validated_data['booking_bus_driver_image'],
            booking_payment_mode = validated_data['booking_payment_mode'],
            booking_school_name = validated_data['booking_school_name'],
            booking_order_id = uuid_id_split,
            )
        return create_booking_order
        
        




    
        