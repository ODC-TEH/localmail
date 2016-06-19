# Local Mail Database

A Python powered website designed for keeping logs of sent and recieved mails with basic CRUD.

### Prerequisites

	- libapache2_mod_wsgi
	- python2.7-dev
	- postgresql
	- python-psycopg2
	- python-pip
	- Flask==0.9
	- SQLAlchemy==0.8.4
	- werkzeug==0.8.3
	- Flask-Login==0.1.3
	 
	
### Quick Start
This guide is based on *Apache HTTP Server* on an *Ubuntu 15.10*:

Enable Apache's *WSGI* module and reload the service:
```sh
sudo a2enmod wsgi
sudo service apache2 reload
```

Created a new database and a new user with access to said database with following commands:
```sh
CREATE DATABASE catalogdb;
CREATE USER catuser;
ALTER ROLE catuser WITH PASSWORD 'catpassword';
GRANT ALL PRIVILEGES ON DATABASE catalogdb TO catuser;
```
Clone or copy *localmail* and *cd* into it; Copy *localmaildbRootfolder* to your *www* root:
```sh
sudo cp -r localmaildbRootfolder /var/www/
```
Copy *localmaildb.conf* file to */etc/apache2/sites-available/* and enable it:
```sh
sudo cp localmaildbRootfolder/localmaildb.conf /etc/apache2/sites-available/
sudo a2ensite localmaildb
```
Create *data* folder in */var/www/* for users to upload their corresponding documents and give owenership to apache2's user *www-data*:
```sh
sudo mkdir /var/www/data
sudo chown -R www-data:www-data /var/www/data
```
Reload apache2 service:
```sh
sudo service apache2 reload
```

### Tech

local-mail-db uses these projects to work properly:

* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [jQuery] - duh

To be completed...

### Todos

 - Multiple Files Upload
 - User Login and Identification

To be completed...





   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>


