import os

from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from datetime import datetime

from sqlalchemy import create_engine, asc, or_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Incoming, Outgoing
from flask import session as login_session
import string

import httplib2
import json
from flask import make_response
import requests

from werkzeug import secure_filename

app = Flask(__name__)


# Create session and connect to DB
engine = create_engine(
	'postgresql://catuser:catpassword@localhost/catalogdb')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



# Application index page consisting of two buttons for '/incoming/' 
# and '/outgoing/' URLs
@app.route('/')
def chooseIncomingOutgoing():
	return render_template('index.html')



# Incoming Page
# Both GET and POST methods are allowed.
@app.route('/incoming/', methods=['GET', 'POST'])
def insertIncoming():
	# If request is POST (Submit button was pressed!).
	if request.method == 'POST':
		# Get uploaded file from incoming.html.
		uploadedFile = request.files['file']
		# Use secure_filename() to secure a filename before storing it 
		# directly on the filesystem.
		safeFileName = secure_filename(uploadedFile.filename)
		# Get incoming.html fields values by their name.
		newItem = Incoming(letter_number=request.form['letter_number'],
			register_date=request.form['register_date'],
			date=request.form['date'],
			from_email=request.form['from_email'],
			subject=request.form['subject'])
		# If letter_number is empty or contains only space.
		if (not request.form['letter_number'] or
			request.form['letter_number'].isspace()):
			# Flash error message.
			flash('Letter Number can not be empty!')
			# Redirect to '/incoming/' URL by calling its function.
			return redirect(url_for('insertIncoming'))
		# Add the new item to session & commit to the database.
		session.add(newItem)
		session.commit()
		# Sepecify path as:
		# /var/www/data/incoming/year/month/day/id.
		path = os.path.join(
			"var", "www", "data", "incoming",
			str(datetime.now().year), 
			str(datetime.now().month), 
			str(datetime.now().day), str(newItem.id))
		# Make directory if it doesn't exist.
		pathExists(path)
		fullPath = os.path.join(path, safeFileName)
		# Save file to path.
		uploadedFile.save(fullPath)
		# Update newItem with file_location and commit.
		newItem.file_location = fullPath.replace("var/www", "../..")
		session.commit()
		# Flash message with newly added item's id as reference number.
		flash('New Item Reference Number is: %s ' % (newItem.id))
		# Redirect to '/incoming/' URL by calling its function.
		return redirect(url_for('insertIncoming'))
	else:
		# If not POST, render incoming.html.
		return render_template('incoming.html')



# Incoming Search Page
# Both GET and POST methods are allowed.
@app.route('/incoming/search/', methods=['GET', 'POST'])
def queryIncoming():
	# If request is POST (Submit button was pressed!).
	if request.method == 'POST':
		# If reference field is empty or contains only space.
		if (not request.form['reference'] or
			request.form['reference'].isspace()):
			# Flash error message.
			flash('Please Enter a reference number!')
			# Redirect to '/incoming/search/' URL 
			# by calling its function.
			return redirect(url_for('queryIncoming'))
		# Get incomingSearch.html reference field value by its name.
		queryItem = request.form['reference']
		# Query Incoming table and filter the results for search term.
		# If the queryItem is not a number, exclude id from search.
		if (is_number(queryItem)):
			items = session.query(Incoming).filter(or_(
				Incoming.id==queryItem,
				Incoming.letter_number==queryItem,
				Incoming.register_date==queryItem,
				Incoming.date==queryItem, Incoming.from_email==queryItem,
				Incoming.subject==queryItem,
				Incoming.file_location==queryItem))
		else:
			items = session.query(Incoming).filter(or_(
				Incoming.letter_number==queryItem,
				Incoming.register_date==queryItem,
				Incoming.date==queryItem, Incoming.from_email==queryItem,
				Incoming.subject==queryItem,
				Incoming.file_location==queryItem))
		# Return the results as a set of items for incomingSearch.html.
		return render_template('incomingSearch.html', items=items)
	else:
		# If not POST (is GET), query Incoming table 
		# and sort the results based on id.
		items = session.query(Incoming).order_by(asc(Incoming.id))
		# Return the results as a set of items for incomingSearch.html.
		return render_template('incomingSearch.html', items=items)



# Outgoing Page
# Both GET and POST methods are allowed.
@app.route('/outgoing/', methods=['GET', 'POST'])
def insertOutgoing():
	# If request is POST (Submit button was pressed!).
	if request.method == 'POST':
		# Get uploaded file from outgoing.html.
		uploadedFile = request.files['file']
		# Use secure_filename() to secure a filename before storing it 
		# directly on the filesystem.
		safeFileName = secure_filename(uploadedFile.filename)
		# Get outgoing.html fields values by their name.
		newItem = Outgoing(date=request.form['date'],
			to_email=request.form['to_email'],
			subject=request.form['subject'])
		# If date is empty or contains only space.
		if not request.form['date'] or request.form['date'].isspace():
			# Flash error message.
			flash('Date can not be empty!')
			# And redirect to '/outgoing/' URL by calling its function.
			return redirect(url_for('insertOutgoing'))
		# Add the new item to session & commit to the database.
		session.add(newItem)
		session.commit()
		# Sepecify path as:
		# /var/www/data/outgoing/year/month/day/id.
		path = os.path.join(
			"var", "www", "data", "outgoing", 
			str(datetime.now().year), 
			str(datetime.now().month), 
			str(datetime.now().day), str(newItem.id))
		# Make directory if it doesn't exist.
		pathExists(path)
		fullPath = os.path.join(path, safeFileName)
		# Save file to path.
		uploadedFile.save(fullPath)
		# Update newItem with file_location and commit.
		newItem.file_location = fullPath.replace("var/www", "../..")
		session.commit()
		# Flash message with newly added item's id as reference number.
		flash('New Item Reference Number is: %s ' % (newItem.id))
		# Redirect to '/outgoing/' URL by calling its function.
		return redirect(url_for('insertOutgoing'))
	else:
		# If not POST, render outgoing.html.
		return render_template('outgoing.html')



# Outgoing Search Page
# Both GET and POST methods are allowed.
@app.route('/outgoing/search/', methods=['GET', 'POST'])
def queryOutgoing():
	# If request is POST (Submit button was pressed!).
	if request.method == 'POST':
		# If reference field is empty or contains only space.
		if (not request.form['reference'] or
			request.form['reference'].isspace()):
			# Flash error message.
			flash('Please Enter a reference number!')
			# Redirect to '/incoming/search/' URL 
			# by calling its function.
			return redirect(url_for('queryOutgoing'))
		# Get outgoingSearch.html reference field value by its name.
		queryItem = request.form['reference']
		# Query Outgoing table and filter the results for search term.
		# If the queryItem is not a number, exclude id from search.
		if (is_number(queryItem)):
			items = session.query(Outgoing).filter(or_(
				Outgoing.id==queryItem,
				Outgoing.date==queryItem, Outgoing.to_email==queryItem,
				Outgoing.subject==queryItem,
				Outgoing.file_location==queryItem))
		else:
			items = session.query(Outgoing).filter(or_(
				Outgoing.date==queryItem, Outgoing.to_email==queryItem,
				Outgoing.subject==queryItem,
				Outgoing.file_location==queryItem))
		# Return the results as a set of items for outgoingSearch.html.
		return render_template('outgoingSearch.html', items=items)
	else:
		# If not POST (is GET), query Outgoing table 
		# and sort the results based on id.
		items = session.query(Outgoing).order_by(asc(Outgoing.id))
		# Return the results as a set of items for outgoingSearch.html.
		return render_template('outgoingSearch.html', items=items)


# Make dir if it doesn't exist.
def pathExists(path):
	if not os.path.exists(path):
		os.makedirs(path)


# Return True if value is a number
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	# App is running in debug mode; Not good in production enviornment! 
	app.debug = True
	app.run()
