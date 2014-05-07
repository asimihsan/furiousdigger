# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Token'
        db.create_table(u'scraper_token', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(unique=True)),
        ))
        db.send_create_signal(u'scraper', ['Token'])

        # Adding model 'UnigramCount'
        db.create_table(u'scraper_unigramcount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scraper.Article'])),
            ('token1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scraper.Token'])),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'scraper', ['UnigramCount'])

        # Adding unique constraint on 'UnigramCount', fields ['article', 'token1']
        db.create_unique(u'scraper_unigramcount', ['article_id', 'token1_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UnigramCount', fields ['article', 'token1']
        db.delete_unique(u'scraper_unigramcount', ['article_id', 'token1_id'])

        # Deleting model 'Token'
        db.delete_table(u'scraper_token')

        # Deleting model 'UnigramCount'
        db.delete_table(u'scraper_unigramcount')


    models = {
        u'scraper.article': {
            'Meta': {'ordering': "('source', '-published', 'url')", 'unique_together': "(('url',),)", 'object_name': 'Article'},
            'extracted_body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'raw_html': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scraper.Source']"}),
            'url': ('django.db.models.fields.TextField', [], {'default': "''", 'db_index': 'True'})
        },
        u'scraper.source': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name',),)", 'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        u'scraper.token': {
            'Meta': {'object_name': 'Token'},
            'content': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'scraper.unigramcount': {
            'Meta': {'unique_together': "(('article', 'token1'),)", 'object_name': 'UnigramCount'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scraper.Article']"}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scraper.Token']"})
        }
    }

    complete_apps = ['scraper']