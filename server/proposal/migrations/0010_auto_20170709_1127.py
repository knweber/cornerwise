# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-09 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0009_auto_20170404_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposals', to='parcel.Parcel'),
        ),
    ]