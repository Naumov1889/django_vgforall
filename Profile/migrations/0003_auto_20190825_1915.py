# Generated by Django 2.2.3 on 2019-08-25 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_auto_20190825_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.CharField(default='', max_length=8),
        ),
    ]
