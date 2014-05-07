# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.url'
        db.add_column('scraper_article', 'url',
                      self.gf('django.db.models.fields.TextField')(default='', db_index=True),
                      keep_default=False)

        # Adding index on 'Source', fields ['name']
        db.create_index('scraper_source', ['name'])


    def backwards(self, orm):
        # Removing index on 'Source', fields ['name']
        db.delete_index('scraper_source', ['name'])

        # Deleting field 'Article.url'
        db.delete_column('scraper_article', 'url')


    models = {
        'scraper.article': {
            'Meta': {'object_name': 'Article'},
            'extracted_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'raw_html': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scraper.Source']"}),
            'url': ('django.db.models.fields.TextField', [], {'default': "''", 'db_index': 'True'})
        },
        'scraper.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['scraper']