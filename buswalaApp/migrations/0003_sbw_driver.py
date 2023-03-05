# Generated by Django 3.2.5 on 2023-03-02 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buswalaApp', '0002_auto_20230223_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='sbw_driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_name', models.CharField(max_length=50)),
                ('bus_no', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=150)),
                ('driver_phone_no', models.CharField(max_length=20)),
                ('driver_email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=500)),
                ('profile', models.ImageField(blank=True, null=True, upload_to='images')),
                ('bus_driver_image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('active_student_count', models.IntegerField(default=0)),
                ('ratings', models.IntegerField(default=0)),
                ('bus_status', models.IntegerField(default=0)),
                ('unique_business_id', models.CharField(max_length=50, unique=True)),
                ('driver_status', models.IntegerField(default=0)),
                ('otp_mob_mail', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]