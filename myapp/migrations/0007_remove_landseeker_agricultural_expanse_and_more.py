# Generated by Django 5.0.6 on 2024-08-11 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_myuser_is_superuser_alter_myuser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landseeker',
            name='agricultural_expanse',
        ),
        migrations.RemoveField(
            model_name='landseeker',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='landseeker',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='landseeker',
            name='last_name',
        ),
        migrations.AddField(
            model_name='landseeker',
            name='agricultural_expanse_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='landseeker',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='landseeker',
            name='pincode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='landseeker',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='landseeker',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='landseeker',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
    ]