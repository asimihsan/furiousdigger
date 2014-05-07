#  ========================================================================
#  furiousdigger: scraper/tasks/models.py
#  Models for the scraper, where aritlces and tokens are gathered.
#  ========================================================================
#  Copyright (c) 2014, Asim Ihsan, All rights reserved.
#  <http://www.asimihsan.com>
#  https://github.com/asimihsan/furiousdigger/blob/master/LICENSE
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  ========================================================================


from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Source(models.Model):
    name = models.CharField(db_index=True, max_length=255)
    url = models.TextField(default='')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', )
        ordering = ('name', )


@python_2_unicode_compatible
class Article(models.Model):
    source = models.ForeignKey(Source)
    url = models.TextField(db_index=True, default='')
    published = models.DateTimeField()
    raw_html = models.TextField(default='')
    extracted_body = models.TextField()

    def __str__(self):
        return self.url

    class Meta:
        unique_together = ('url', )
        ordering = ('source', '-published', 'url')


@python_2_unicode_compatible
class Token(models.Model):
    content = models.TextField(unique=True)

    @property
    def total_count(self):
        return UnigramCount.objects.filter(token1__content=self.content) \
                                   .aggregate(models.Sum('count')).values()[0]

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('content', )


@python_2_unicode_compatible
class UnigramCount(models.Model):
    article = models.ForeignKey(Article, db_index=True)
    token1 = models.ForeignKey(Token, db_index=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return "{article=%s, token1=%s, count=%s}" % (self.article, self.token1, self.count)

    class Meta:
        unique_together = ('article', 'token1')
