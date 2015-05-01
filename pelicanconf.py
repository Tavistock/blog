#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Travis McNeill'
SITENAME = u'tavistock'
SITEURL = ''
SIGNATURE = 'travis mcneill &#8756 tavistock91@gmail.com'

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
SOCIAL = (('@github', 'https://github.com/Tavistock'),
        ('@twitter', 'https://twitter.com/tavistock_esq'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'themes/paperlite'

ATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
        'extra/robots.txt': {'path': 'robots.txt'},
        'extra/favicon.ico': {'path': 'favicon.ico'}
        }
