#  ========================================================================
#  furiousdigger: scraper/tasks/admin.py
#  Admin config for scraper models.
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

from django.contrib import admin
from scraper.models import Source, Article, Token, UnigramCount


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('source', 'published', 'url')
    list_filter = ['source', 'published']
    search_fields = ['extracted_body']


class TokenAdmin(admin.ModelAdmin):
    list_display = ('content', 'total_count')
    search_fields = ['content']


class UnigramCountAdmin(admin.ModelAdmin):
    list_display = ('article', 'token1', 'count')
    list_filter = ['article__source', 'count']
    search_fields = ['token1__content']

admin.site.register(Source)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(UnigramCount, UnigramCountAdmin)
