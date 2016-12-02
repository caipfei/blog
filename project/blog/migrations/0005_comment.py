# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 01:43
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20161124_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='内容')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now, verbose_name='发表时间')),
                ('disabled', models.BooleanField(default=False, verbose_name='是否禁用')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post', verbose_name='文章')),
            ],
        ),
    ]
