import sys 
import os 
import unittest
import time

sys.path.append(os.path.abspath('..'))

import yaml
import requests

from app.server import load_app

configpath=os.path.dirname(__file__) + "/../config/local.yaml"
config = yaml.safe_load(open(configpath))

class TestDerivGeneration(unittest.TestCase):
    """
    Test admin tools.
    """

    app = load_app(config["app_base_path"] + "config/local.yaml", config["app_base_path"] +  "config/profiles.yaml")
    
    def setUp(self):
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.ctx.pop()
        if os.path.exists(config["app_base_path"] + "data/derivatives/20_1210994.jpg_jpg2jpg.jpg"):
            os.remove(config["app_base_path"] + "data/derivatives/20_1210994.jpg_jpg2jpg.jpg")
        if os.path.exists(config["app_base_path"] + "data/derivatives/addison_sunrise.tif_d12ptiff.tif"):
            os.remove(config["app_base_path"] + "data/derivatives/addison_sunrise.tif_d12ptiff.tif")
        if os.path.exists(config["app_base_path"] + "data/derivatives/addison_sunrise.tif_d12jpeg2000.jp2"):
            os.remove(config["app_base_path"] + "data/derivatives/addison_sunrise.tif_d12jpeg2000.jp2")

    def test_list_profiles(self):
        response = self.client.get("/profiles/list")
        assert response.status_code == 200

    def test_jpg2jpg(self):
        source_image = config["app_base_path"] + "tests/assets/20_1210994.jpg"
        response = self.client.get("/profiles/jpg2jpg/convert?source=" + source_image)
        assert response.status_code == 200
        
    def test_d12ptiff(self):
        source_image = config["app_base_path"] + "tests/assets/addison_sunrise.tif"
        response = self.client.get("/profiles/d12ptiff/convert?source=" + source_image)
        assert response.status_code == 200

    def test_d12jpeg2000(self):
        source_image = config["app_base_path"] + "tests/assets/addison_sunrise.tif"
        response = self.client.get("/profiles/d12jpeg2000/convert?source=" + source_image)
        assert response.status_code == 200


