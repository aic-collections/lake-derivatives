import os
import sys
import yaml
import json

import requests

from flask import g

from flask import Flask
from flask import request
from flask import Response, redirect, send_file

import logging
import logging.config
from logging import getLogger

sys.path.append(os.path.abspath('..'))

from modules.convert import Convert

app = Flask(__name__)
profiles = None
config = None


@app.route("/profiles/<profile_id>/convert")
def profile_convert(profile_id):
    
    profile = profiles[profile_id]
    source_file = str(request.args.get('source'))
    output_filename = str(request.args.get('output_filename'))
    
    convert = Convert(config, profile, profile_id)
    result = convert.convert(source_file)
    
    if result["status"] == "success":
        return send_file(result["derivative_path"], as_attachment=True)
    else:
        response = Response("Something went wrong - " + result["status"])
        response.headers['Content-type'] = "text/plain"
        return (response, 500)


@app.route("/profiles/<profile_id>/view")
def profile_view(profile_id):
    profile = profiles[profile_id]
    profile_json = json.dumps(profile, sort_keys=True, indent=4)
    response = Response(profile_json)
    response.headers['Content-type'] = "application/json"
    return (response, 200)


@app.route("/profiles/list")
def profiles():
    profiles_json = json.dumps(profiles, sort_keys=True, indent=4)
    response = Response(profiles_json)
    response.headers['Content-type'] = "application/json"
    return (response, 200)

def load_app(configpath, profilespath):
    global config, profiles
    config = yaml.safe_load(open(configpath))
    profiles = yaml.safe_load(open(profilespath))
    
    if not config["tmp_dirs"]["source"].startswith('/'):
        config["tmp_dirs"]["source"] = config["app_base_path"] + config["tmp_dirs"]["source"]
    
    if not config["tmp_dirs"]["tmpsources"].startswith('/'):
        config["tmp_dirs"]["tmpsources"] = config["app_base_path"] + config["tmp_dirs"]["tmpsources"]
    
    if not config["tmp_dirs"]["output"].startswith('/'):
        config["tmp_dirs"]["output"] = config["app_base_path"] + config["tmp_dirs"]["output"]

    logging.config.dictConfig(config["logging"])
    logging.info('Started')
    logger = getLogger(__name__)

    logger.info("Application loaded using config: {}".format(config))
    logger.info("Application loaded using profiles: {}".format(profiles))
    return app

if __name__ == "__main__":
    from modules.config_parser import args
    config = yaml.safe_load(open(args.config))
    profiles = yaml.safe_load(open(args.profiles))
    
    if not config["tmp_dirs"]["sources"].startswith('/'):
        config["tmp_dirs"]["sources"] = config["app_base_path"] + config["tmp_dirs"]["sources"]
    
    if not config["tmp_dirs"]["tmpsources"].startswith('/'):
        config["tmp_dirs"]["tmpsources"] = config["app_base_path"] + config["tmp_dirs"]["tmpsources"]
    
    if not config["tmp_dirs"]["derivatives"].startswith('/'):
        config["tmp_dirs"]["derivatives"] = config["app_base_path"] + config["tmp_dirs"]["derivatives"]

    logging.config.dictConfig(config["logging"])
    logging.info('Started')
    logger = getLogger(__name__)

    logger.info("Application loaded using config: {}".format(config))
    app.run(debug=True, host="0.0.0.0", port=8010)

