# About

Lake Derivatives generates derivatives.  It fetches content from Fedora and converts
it per a profile setting.  

See the profiles in the `profiles.yaml` file for pre-configured profiles.

This software expects the following to be installed on the host machine:
    imagemagick
    ffmpeg

NB (2018-09-28):  This code is predicated on Fedora not requiring authentication.
That has changed (Fedora requires authentication) but this code has not.

# Getting Started

~~~bash
virtualenv -p python3 ldenv
cd ldenv
. bin/activate
git clone https://github.com/aic-collections/lake-derivatives.git
cd lake-derivatives
pip install -r requirements.txt
~~~

At this point you will need to modify at least one file to get going:

~~~bash
cp config/profiles.yaml.default config/profiles.yaml
cp config/local.yaml.default config/local.yaml
~~~
Open the files for editing and make changes as needed.  Minimally, 
the `app_base_path` base in `local.yaml` value will have to be changed.  The 
remaining should be OK to get going.

You can now start Lake Derivatives:

~~~bash
./bin/flask-server.sh start
~~~

NB: The above command is predicated on not altering the location of the config 
file *and* maintaining its current name (config.yaml).

# API

- GET `/profiles/list` - List available profiles.  
- GET `/profiles/<profile_id>/view` - View a specific profile. 
- GET `/profiles/<profile_id>/convert` - Execute a specific profile.

# Running in production

Gunicorn - a WSGI HTTP Server - can be used for production.  You will need to modify
at least two additional files:

~~~bash
cp config/gunicorn_prod.py.default config/gunicorn_prod.py
cp app/wsgi.py.default app/wsgi.py
~~~

Open each file and edit as needed.

# License

[AIC Copyright; Apache License 2.0](LICENSE)



