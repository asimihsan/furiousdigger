# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Article', fields ['url']
        db.create_unique('scraper_article', ['url'])

        # Adding unique constraint on 'Source', fields ['name']
        db.create_unique('scraper_source', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Source', fields ['name']
        db.delete_unique('scraper_source', ['name'])

        # Removing unique constraint on 'Article', fields ['url']
        db.delete_unique('scraper_article', ['url'])


    models = {
        'scraper.article': {
            'Meta': {'unique_together': "(('url',),)", 'object_name': 'Article'},
            'extracted_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'raw_html': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scraper.Source']"}),
            'url': ('django.db.models.fields.TextField', [], {'default': "''", 'db_index': 'True'})
        },
        'scraper.source': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['scraper']