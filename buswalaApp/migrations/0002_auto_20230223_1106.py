# Generated by Django 3.2.5 on 2023-02-23 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buswalaApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sbw_customer',
            name='customer_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sbw_customer',
            name='otp_mob_mail',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
