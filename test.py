#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.settimeout(1)
try:
  sk.connect(('10.254.5.8',3307))
  print 'Server port 80 OK!'
except Exception:
  print 'Server port 80 not connect!'
sk.close()
