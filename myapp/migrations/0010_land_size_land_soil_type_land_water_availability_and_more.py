# Generated by Django 5.0.6 on 2024-08-25 07:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_userprofile_gender_userprofile_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='land',
            name='size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='land',
            name='soil_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='land',
            name='water_availability',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Landowner',
            fields=[
                ('landowner_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='landowner_photos/')),
                ('gender', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='landowner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='land',
            name='landowner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lands', to='myapp.landowner'),
        ),
    ]
