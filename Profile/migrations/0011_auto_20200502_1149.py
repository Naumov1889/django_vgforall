# Generated by Django 2.2.6 on 2020-05-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0010_callback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callback',
            name='text',
            field=models.TextField(verbose_name='Вопрос'),
        ),
    ]
