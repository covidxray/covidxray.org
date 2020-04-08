# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app import app, db



app.config.update(
  PREFERRED_URL_SCHEME = 'https'
  TESTING=False,
  DEBUG = False,
  SECRET_KEY=b'1_5#y2L"F4Q8z\n\xec]/'
)