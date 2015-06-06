#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Travis McNeill'
SITENAME = u'Travis McNeill'
TAGLINE = 'Embrace Uncertainty'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('dosync', 'http://swannodette.github.io/'),
        ('rigsomelight', 'http://rigsomelight.com/'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/Tavistock'),
          ('Twitter', 'https://twitter.com/tavistock_esq'),)

TWITTER_USERNAME = 'https://twitter.com/tavistock_esq'
USER_LOGO_URL = 'images/logo.svg'

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'themes/pelican-svbtle-responsive'

STATIC_PATHS = ['images','voxel', 'extra/robots.txt']
EXTRA_PATH_METADATA = {
        'extra/robots.txt': {'path': 'robots.txt'},
        }
