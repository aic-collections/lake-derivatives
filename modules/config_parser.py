import argparse
import os

parser = argparse.ArgumentParser(description = 'LAKE Derivatives.')
parser.add_argument('-c', '--config', default=os.path.dirname(__file__) + "/../config/local.yaml", help='Configuration file path.')
parser.add_argument('-p', '--profiles', default=os.path.dirname(__file__) + "/../config/profiles.yaml", help='Profiles file path.')

args = parser.parse_args()
