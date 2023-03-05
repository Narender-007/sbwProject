# Generated by Django 3.2.5 on 2023-03-03 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('buswalaApp', '0004_auto_20230303_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='sbw_bookingOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('booking_status', models.IntegerField(default=0)),
                ('booking_price', models.IntegerField(default=0)),
                ('booking_bus_no', models.CharField(max_length=50)),
                ('booking_bus_location', models.CharField(max_length=50)),
                ('booking_bus_image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('booking_bus_status', models.IntegerField(default=0)),
                ('booking_bus_driver_image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('booking_payment_mode', models.CharField(max_length=100)),
                ('booking_school_name', models.CharField(max_length=100)),
                ('booking_order_id', models.CharField(max_length=100)),
                ('booking_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('booking_driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buswalaApp.sbw_driver')),
            ],
        ),
    ]
