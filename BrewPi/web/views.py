from flask import send_from_directory, request, redirect, url_for, abort, render_template
from BrewPi.data.database import db_session
from BrewPi.data.models import Recipes, Steps, Vessels
from json_out import json_as_configured
from sqlalchemy import or_
from app import app

@app.route('/')
def index():
	return send_from_directory(app.static_folder,'api.html')

@app.route('/vessel/<id>')
def show_kettle(id):
    kettle = Vessels.query.get(id);
    if kettle == None:
        return json_as_configured({'ErrorCode':404,'ErrorMsg':'Item not found'})
    else:
        return json_as_configured(kettle.serialize())

@app.route('/step/<id>')
def show_step(id):
    step = Steps.query.get(id);
    if step == None:
        return json_as_configured({'ErrorCode':404,'ErrorMsg':'Item not found'})
    else:
        return json_as_configured(step.serialize())

@app.route('/recipe/<id>')
def show_recipe(id):
    recipe = Recipes.query.get(id);
    if recipe == None:
        return json_as_configured({'ErrorCode':404,'ErrorMsg':'Item not found'})
    else:
        r = recipe.serialize()
        step = Steps.query.get(recipe.currentStepID)
        r['currentStep'] = None
        if step != None:
            r['currentStep'] = step.serialize()
        return json_as_configured(r)

@app.route('/vessel/', methods=['GET', 'POST'])
def write_kettle():
    if request.method == 'GET':
        if request.args.get('id'):
            return redirect(url_for('show_vessel', id=request.args.get('id')))
        else:
            abort(400)

    kettle = Vessels(
                 vesselID=request.json.get('vesselID', None),
                 name=request.json.get('name', '')
                 )
    db_session.add(kettle)

    return json_as_configured(kettle.serialize())
