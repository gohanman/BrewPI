from flask import json, jsonify
from .. import config

def json_as_configured(dict):
	if type(dict) == type([]):
		dict = { 'results' : dict }
	if config.JSON_HEADERS:
		return jsonify(dict)
	else:
		return json.dumps(dict)
