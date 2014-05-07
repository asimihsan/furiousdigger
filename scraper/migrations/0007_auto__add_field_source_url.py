# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Source.url'
        db.add_column('scraper_source', 'url',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Source.url'
        db.delete_column('scraper_source', 'url')


    models = {
        'scraper.article': {
            'Meta': {'unique_together': "(('url',),)", 'object_name': 'Article'},
            'extracted_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'raw_html': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scraper.Source']"}),
            'url': ('django.db.models.fields.TextField', [], {'default': "''", 'db_index': 'True'})
        },
        'scraper.source': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['scraper']