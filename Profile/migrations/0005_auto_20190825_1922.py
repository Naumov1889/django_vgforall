# Generated by Django 2.2.3 on 2019-08-25 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0004_auto_20190825_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city_of_residence',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='country_of_residence',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.CharField(default='', max_length=8),
        ),
    ]
