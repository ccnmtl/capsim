# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RunRecord'
        db.create_table('sim_runrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default=u'', null=True, blank=True)),
        ))
        db.send_create_signal('sim', ['RunRecord'])


    def backwards(self, orm):
        # Deleting model 'RunRecord'
        db.delete_table('sim_runrecord')


    models = {
        'sim.runrecord': {
            'Meta': {'object_name': 'RunRecord'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "u''", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['sim']
