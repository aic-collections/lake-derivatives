import os
import glob
import errno
import re
import uuid
import subprocess
import requests

from logging import getLogger

from flask import Response

class Convert:

    config = None
    profile = None
    profile_id = ""
    source_path = ""
    source_mime = ""
    
    mimemap = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/tiff": "tif",
        "image/jp2": "jp2",
        "audio/mpeg": "mp3",
        "video/x-flv": "flv",
        "video/mpeg": "mpeg",
        "application/pdf": "pdf",
    }
    
    def __init__(self, config, profile, profile_id):
        self.logger = getLogger(__name__)
        
        self.config = config
        self.profile = profile
        self.profile_id = profile_id
        
        self.source_mimetype = self.profile["source_mimetype"]
        
        self.logger.debug("Convert profile is: {}".format(self.profile))
        return
    

    def convert(self, source_file):
        # Fetch content
        #   Capture source mimetype
        #   Store in source directory
        #
        # Perform conversion
        # Return what?  
        
        if source_file.startswith("http"):
            # Must fetch content from URI
            auth=("user", "password")
            if "lakesuperior.artic.edu/fcrepo/" in source_file:
                auth=(self.config["lake_fcrepo"]["user"], self.config["lake_fcrepo"]["pass"])
            
            self.session = requests.Session()
            with self.session.get(source_file, auth=auth, stream=True) as r:
                # print(str(r.status_code))
                if r.status_code == 404:
                    response_object = {
                        "status": "404 Source Not Found"
                    }
                    return response_object
                if r.status_code == 500:
                    response_object = {
                        "status": "500 Source Server Error"
                    }
                    return response_object

                if 'content-type' in r.headers:
                    self.source_mimetype = r.headers["content-type"]
                
                fname = ""
                if 'content-disposition' in r.headers:
                    cd = r.headers['content-disposition']
                    cd_parts = cd.split(';')
                
                    for p in cd_parts:
                        if p.strip().startswith('filename'):
                            fname = re.findall("filename=(.+)", p)[0]
                            fname = fname.replace('"', '')
                if fname == "":
                    fname = str(uuid.uuid4()) + '.' + self.mimemap[self.source_mimetype]
                
                self.source_path = self.config["tmp_dirs"]["sources"] + fname
                with open(self.source_path, 'wb') as f:
                    # Increase the chunk size.  Fewer disk writes.
                    for chunk in r.iter_content(10240):
                        f.write(chunk)
                
        elif source_file.startswith("/"):
            self.source_path = source_file
            source_file_parts = source_file.split('/')
            fname = source_file_parts[-1]
        
        else: 
            # We have a problem, Tex.
            response_object = {
                "status": "Error: Invalid source file, niether begins with 'http' or '/'.",
            }
            
        
        cmd = self.profile["cmd"]
        cmd = cmd.replace('%SOURCE%', self.source_path)
        derivative_filename = fname + "_" + self.profile_id + '.' + self.mimemap[self.profile["derivative_mimetype"]]
        derivative_path = self.config["tmp_dirs"]["derivatives"] + derivative_filename
        # print(derivative_path)
        cmd = cmd.replace('%DERIVATIVE%', derivative_path)
        if '%TMPSOURCE%' in cmd:
            tmpfile = self.config["tmp_dirs"]["tmpsources"] + fname
            cmd = cmd.replace('%TMPSOURCE%', tmpfile)
        try:
            output = subprocess.check_output(cmd, shell=True)
            # print(output.decode("utf8"))
                
            json_response = '{"status": "success"}'
            #response = Response(json_response, status=200)
            #response.headers['Content-type'] = "application/json"
            #return response
            
        except subprocess.CalledProcessError as err:
            error_msg = "Return code: {}; Cmd: {}; Output: {}".format(err.returncode, err.cmd, err.output)
                
            json_response = '{"status": "Error - ' + error_msg + '"}'
            response = Response(json_response, status=500)
            response.headers['Content-type'] = "application/json"
            return response
            
            raise
    
        #with open(derivative_path, 'rb') as f:
        #    content = f.read()
        
        response_object = {
            "status": "success",
            "filename": derivative_filename,
            "derivative_path": derivative_path, 
            "mimetype": self.profile["derivative_mimetype"]
        }
        return response_object
        
