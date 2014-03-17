# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InterventionLevel'
        db.create_table(u'sim_interventionlevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('intervention', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sim.Intervention'])),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('cost', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'sim', ['InterventionLevel'])

        # Adding model 'Modifier'
        db.create_table(u'sim_modifier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interventionlevel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sim.InterventionLevel'])),
            ('parameter', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('adjustment', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'sim', ['Modifier'])

        # Adding model 'Intervention'
        db.create_table(u'sim_intervention', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=256)),
        ))
        db.send_create_signal(u'sim', ['Intervention'])


    def backwards(self, orm):
        # Deleting model 'InterventionLevel'
        db.delete_table(u'sim_interventionlevel')

        # Deleting model 'Modifier'
        db.delete_table(u'sim_modifier')

        # Deleting model 'Intervention'
        db.delete_table(u'sim_intervention')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sim.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'completed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "u''", 'null': 'True', 'blank': 'True'}),
            'dependent_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dependent_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dependent_steps': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'dependent_variable': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'independent_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'independent_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'independent_steps': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'independent_variable': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'enqueued'", 'max_length': '256'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "u''", 'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'trials': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'sim.exprun': {
            'Meta': {'object_name': 'ExpRun'},
            'dependent_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sim.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'independent_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'default': "'100.0'"}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sim.RunRecord']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'enqueued'", 'max_length': '256'}),
            'trial': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'sim.intervention': {
            'Meta': {'object_name': 'Intervention'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '256'})
        },
        u'sim.interventionlevel': {
            'Meta': {'object_name': 'InterventionLevel'},
            'cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervention': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sim.Intervention']"}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'sim.modifier': {
            'Meta': {'object_name': 'Modifier'},
            'adjustment': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interventionlevel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sim.InterventionLevel']"}),
            'parameter': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'sim.runoutputrecord': {
            'Meta': {'object_name': 'RunOutputRecord'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "u''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sim.RunRecord']"})
        },
        u'sim.runrecord': {
            'Meta': {'object_name': 'RunRecord'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "u''", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "u''", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['sim']
