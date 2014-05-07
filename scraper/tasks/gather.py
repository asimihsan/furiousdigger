#!/usr/bin/env python

#  ========================================================================
#  furiousdigger: scraper/tasks/gather.py
#  Given RSS feeds gather article content and tokens using handytrowel.
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


import collections
import dateutil.parser
import feedparser
import json
import os
import random
import requests
import requests_cache
import subprocess
import sys

import django.utils.timezone
from six.moves import configparser

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'furiousdigger.settings'
from django.db.models.loading import get_models
loaded_models = get_models()

from scraper.models import Article, Source, Token, UnigramCount


FURIOUS_DIGGER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
SCRAPER_FEEDS_CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "scraper_feeds.ini"))
HANDY_TROWEL_BIN = os.path.abspath(
    os.path.join(FURIOUS_DIGGER_ROOT, os.pardir,
                 "handytrowel/build/install/handytrowel/bin/handytrowel"))

import logging
logger = logging.getLogger('scraper.tasks.gather')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

log_dir = os.path.expanduser(os.path.join(FURIOUS_DIGGER_ROOT, "log"))
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
fh = logging.handlers.RotatingFileHandler(os.path.join(log_dir, 'gather.log'),
                                          maxBytes=1024 * 1024 * 5,
                                          backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def scrape_article(url):
    logger.debug("scraping article at URL: %s" % url)
    assert(os.path.isfile(HANDY_TROWEL_BIN))
    output = {}
    try:
        output = json.loads(subprocess.check_output([HANDY_TROWEL_BIN, url]))
    except subprocess.CalledProcessError as e:
        logger.exception("scraper threw exception with output: '%s'" % e.output.strip())
    return output


def scrape_feed(source, url, max_entries=20):
    logger.debug("scrape_feed entry. source: %s, url: %s" % (source, url))
    request = requests.get(url)
    request.raise_for_status()
    feed = feedparser.parse(request.text)
    for (i, entry) in enumerate(feed["entries"]):
        if i + 1 >= max_entries:
            logger.info("scraped maximum number of entries.")
            return

        link = entry["link"]
        logger.info("HTTP HEAD for URL %s to resolve redirects..." % link)
        request = requests.head(link, allow_redirects=True, timeout=10)
        request.raise_for_status()
        redirected_link = request.url
        logger.info("link after redirection: %s" % redirected_link)

        if Article.objects.filter(url=redirected_link).exists():
            logger.info("skipping URL that already exists")
            continue
        contents = scrape_article(redirected_link)
        if len(contents.get("extractedBody", "")) == 0:
            logger.info("skipping URL with no contents.")
            continue
        kwargs = {"source": source, "url": redirected_link,
                  "extracted_body": contents["extractedBody"]}
        for date_key in ["published"]:
            if date_key in entry:
                logger.info("published date for this link is known")
                kwargs["published"] = dateutil.parser.parse(entry[date_key])
        if "published" not in kwargs:
            logger.info("published date for this link is not known")
            kwargs["published"] = django.utils.timezone.now()
        article, _ = Article.objects.get_or_create(**kwargs)

        token_counts = collections.defaultdict(int)
        for token in contents["tokens"]:
            token_counts[token] += 1
        unigram_counts = []
        logger.info("updating token counts for article...")
        for (token, count) in token_counts.iteritems():
            token, _ = Token.objects.get_or_create(content=token)
            unigram_counts.append(UnigramCount(article=article,
                                               token1=token,
                                               count=count))
        UnigramCount.objects.bulk_create(unigram_counts)
        logger.info("updated token counts for article...")
    logger.info("scrape_feed exit. source: %s, url: %s" % (source, url))


def load_config(path=SCRAPER_FEEDS_CONFIG_PATH):
    assert(os.path.isfile(path))
    config = configparser.SafeConfigParser()
    config.read(path)
    return config


def main():
    requests_cache.install_cache(
        os.path.join(FURIOUS_DIGGER_ROOT, 'requests_cache'),
        expire_after=30 * 60)
    config = load_config()
    sections = config.sections()
    random.shuffle(sections)
    for section in sections:
        logger.info("main: starting processing section %s" % section)
        source_object, _ = Source.objects.get_or_create(name=section)
        try:
            logger.info("main: update feed URL")
            feed_config = dict(config.items(section))
            source_object.url = feed_config["url"]
            source_object.save()
            logger.info("main: call scrape_feed...")
            scrape_feed(source=source_object, url=feed_config["url"])
            logger.info("main: finished calling scrape_feed")
        except:
            logger.exception("unhandled exception for feed: %s" % feed_config)


if __name__ == "__main__":
    logger.info("starting")
    sys.exit(main())
    logger.info("exiting")
