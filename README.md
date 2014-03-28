ADL xAPI / Medbiquitous Competency Example
==================

## Requirements
* Python 2.7
* Mongo DB
* lxml

## Installing (Ubuntu)

1. Install the system dependencies

	```bash
	$ sudo apt-get install git python-pip mongodb-server libxml2-dev libxslt1-dev zlib1g-dev python-dev
	```

2. Set up the development environment

	```bash
	$ sudo pip install --upgrade pip
	$ sudo pip install virtualenv
	
	$ git clone https://github.com/adlnet/competency-example.git
	$ cd competency-example
	$ virtualenv env
	$ pip install -r requirements.txt
	```

3. Configuration

	Edit the settings.py in the util directory.  Enter valid xAPI endpoint credentials.  I pointed to the public LRS with my LRS username and password:
	
	[https://lrs.adlnet.gov/xAPI/statements](https://lrs.adlnet.gov/xAPI/statements)

## Running

```bash
$ cd competency-example
$ source env/bin/activate
$ python main.py
```

To leave the virtualenv: `$ deactivate`
