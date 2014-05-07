# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Article.published'
        db.alter_column('scraper_article', 'published', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):

        # Changing field 'Article.published'
        db.alter_column('scraper_article', 'published', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        'scraper.article': {
            'Meta': {'object_name': 'Article'},
            'extracted_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'raw_html': ('django.db.models.fields.TextField', [], {'default': "''"}),
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