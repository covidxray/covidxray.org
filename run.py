# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app import app, db

app.config.update(dict(
  PREFERRED_URL_SCHEME = 'https'
))