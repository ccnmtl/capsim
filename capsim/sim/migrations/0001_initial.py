# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(default='', null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'enqueued', max_length=256)),
                ('data', models.TextField(default='', null=True, blank=True)),
                ('independent_variable', models.CharField(default=b'', max_length=256, null=True, blank=True)),
                ('dependent_variable', models.CharField(default=b'', max_length=256, null=True, blank=True)),
                ('independent_min', models.FloatField(null=True, blank=True)),
                ('independent_max', models.FloatField(null=True, blank=True)),
                ('independent_steps', models.IntegerField(default=1, null=True, blank=True)),
                ('dependent_min', models.FloatField(null=True, blank=True)),
                ('dependent_max', models.FloatField(null=True, blank=True)),
                ('dependent_steps', models.IntegerField(default=1, null=True, blank=True)),
                ('trials', models.IntegerField(default=1)),
                ('total', models.IntegerField(default=0)),
                ('completed', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExpRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'enqueued', max_length=256)),
                ('independent_value', models.FloatField(null=True, blank=True)),
                ('dependent_value', models.FloatField(null=True, blank=True)),
                ('trial', models.IntegerField(default=0)),
                ('mass', models.FloatField(default=b'100.0')),
                ('experiment', models.ForeignKey(to='sim.Experiment', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InterventionLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=256, choices=[(b'high', b'high'), (b'medium', b'medium'), (b'low', b'low')])),
                ('cost', models.IntegerField(default=0)),
                ('intervention', models.ForeignKey(to='sim.Intervention', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Modifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parameter', models.CharField(max_length=256)),
                ('adjustment', models.FloatField(default=0.0)),
                ('interventionlevel', models.ForeignKey(to='sim.InterventionLevel', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=256)),
                ('num_type', models.CharField(max_length=256, choices=[(b'float', b'floating point'), (b'int', b'integer')])),
                ('value', models.FloatField(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RunOutputRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('data', models.TextField(default='', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RunRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('data', models.TextField(default='', null=True, blank=True)),
                ('title', models.TextField(default='', null=True, blank=True)),
                ('description', models.TextField(default='', null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='runoutputrecord',
            name='run',
            field=models.ForeignKey(to='sim.RunRecord', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exprun',
            name='run',
            field=models.ForeignKey(to='sim.RunRecord', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
