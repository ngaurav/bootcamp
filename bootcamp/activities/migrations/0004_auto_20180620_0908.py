# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20180617_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='question',
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(choices=[('L', 'Like')], max_length=1),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('L', 'Liked'), ('C', 'Commented'), ('E', 'Edited Article'), ('A', 'Also Commented'), ('S', 'Shared'), ('I', 'Logged In'), ('O', 'Logged Out')], max_length=1),
        ),
    ]
