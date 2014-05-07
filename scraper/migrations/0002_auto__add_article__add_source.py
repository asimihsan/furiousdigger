# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table('scraper_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scraper.Source'])),
            ('published', self.gf('django.db.models.fields.DateTimeField')()),
            ('raw_html', self.gf('django.db.models.fields.TextField')()),
            ('extracted_body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('scraper', ['Article'])

        # Adding model 'Source'
        db.create_table('scraper_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('scraper', ['Source'])


    def backwards(self, orm):
        # Deleting model 'Article'
        db.delete_table('scraper_article')

        # Deleting model 'Source'
        db.delete_table('scraper_source')


    models = {
        'scraper.article': {
            'Meta': {'object_name': 'Article'},
            'extracted_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'raw_html': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scraper.Source']"})
        },
        'scraper.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['scraper']