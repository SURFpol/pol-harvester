# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-02-05 12:05
from __future__ import unicode_literals

import datagrowth.configuration.fields
from django.db import migrations, models
import django.db.models.deletion
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('edurep', '0005_edurepsource_collection_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='EdurepOAIPMH',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(db_index=True, default=None, max_length=255)),
                ('status', models.PositiveIntegerField(default=0)),
                ('config', datagrowth.configuration.fields.ConfigurationField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('purge_at', models.DateTimeField(blank=True, null=True)),
                ('retainer_id', models.PositiveIntegerField(blank=True, null=True)),
                ('data_hash', models.CharField(db_index=True, default='', max_length=255)),
                ('request', json_field.fields.JSONField(default=None, help_text='Enter a valid JSON object')),
                ('head', json_field.fields.JSONField(default='{}', help_text='Enter a valid JSON object')),
                ('body', models.TextField(blank=True, default=None, null=True)),
                ('retainer_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Edurep OAIPMH harvest',
                'verbose_name_plural': 'Edurep OAIPMH harvests',
            },
        ),
        migrations.AlterField(
            model_name='edurepsource',
            name='collection_name',
            field=models.CharField(help_text='This name will be given to the collection holding all documents for this source. When dealing with OAI-PMH this value will be the setSpec value', max_length=255),
        ),
        migrations.AlterField(
            model_name='edurepsource',
            name='query',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
