# Generated by Django 2.1.1 on 2018-09-18 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180911_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('teacher', 'Teacher'), ('qdt', 'Quality & Design Team')], max_length=10),
        ),
    ]