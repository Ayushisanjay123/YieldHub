# Generated by Django 5.0.6 on 2024-08-25 08:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_land_size_land_soil_type_land_water_availability_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='landseeker',
            name='crop_requirements',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='landseeker',
            name='desired_land_size',
            field=models.FloatField(default='0'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='land',
            name='landowner',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='lands', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='land',
            name='size',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='land',
            name='soil_type',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('land_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communications', to='myapp.landseeker')),
                ('landowner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expressed_interest_date', models.DateTimeField(auto_now_add=True)),
                ('land', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.land')),
                ('land_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.landseeker')),
            ],
        ),
        migrations.AddField(
            model_name='landseeker',
            name='interests',
            field=models.ManyToManyField(through='myapp.Interest', to='myapp.land'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('land_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='myapp.landseeker')),
                ('landowner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
