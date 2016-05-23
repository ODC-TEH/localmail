#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)

# Add path to the application (at the root level) to SYSTEM PATH 
sys.path.insert(0,"/var/www/localmaildbRootfolder/")

# From application folder which containts the main application script
# (localmaildb.py) import app (defined in localmaildb.py)
from localmaildbAppfolder.localmaildb import app as application

# Using the application secret key defined in localmaildb.py
application.secret_key = 'super_secret_key'
