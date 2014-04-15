from flask import send_from_directory, request, redirect, url_for, abort, render_template
from BrewPi.data.database import db_session
from BrewPi.data.models import Recipes, Steps, Vessels, Pumps, Valves, Heaters, Coolers, Plumbing
from json_out import json_as_configured
from sqlalchemy import or_
from app import app

@app.route('/')
def index():
	return send_from_directory(app.static_folder,'api.html')

@app.route('/vessel/<id>')
def show_vessel(id):
    kettle = Vessels.query.get(id);
    if kettle == None:
        return json_as_configured({'ErrorCode':404,'ErrorMsg':'Item not found'})
    else:
        return json_as_configured(kettle.serialize())

@app.route('/pump/<id>')
def show_pump(id):
    obj = Pumps.query.get(id);
    if obj == None:
        return json_as_configured({'ErrorCode':404,'ErrorMsg':'Item not found'})
    else:
        return json_as_configured(obj.serialize())

@app.route('/valve/<id>')
def show_valve(id):
    obj = Valves.query.get(id);
    if obj == None:
        return json_as_configured({'ErrorCode':404,'ErrorMsg':'Item not found'})
    else:
        return json_as_configured(obj.serialize())

@app.route('/heater/<id>')
def show_heater(id):
    obj = Heaters.query.get(id);
    if obj == None:
        return json_as_configured({'ErrorCode':404,'ErrorMsg':'Item not found'})
    else:
        return json_as_configured(obj.serialize())

@app.route('/coolers/<id>')
def show_cooler(id):
    obj = Coolers.query.get(id);
    if obj == None:
        return json_as_configured({'ErrorCode':404,'ErrorMsg':'Item not found'})
    else:
        return json_as_configured(obj.serialize())

@app.route('/plumbing/<id>')
def show_plumbing(id):
    obj = Plumbing.query.get(id);
    if obj == None:
        return json_as_configured({'ErrorCode':404,'ErrorMsg':'Item not found'})
    else:
        return json_as_configured(obj.serialize())

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

        return json_as_configured(r)

@app.route('/setup/')
def show_setup():
    repr = {}
    repr['vessels'] = [v.serialize() for v in Vessels.query.all()]
    repr['pumps'] = [p.serialize() for p in Pumps.query.all()]
    repr['valves'] = [v.serialize() for v in Valves.query.all()]
    repr['heaters'] = [h.serialize() for h in Heaters.query.all()]
    repr['coolers'] = [c.serialize() for c in Coolers.query.all()]
    repr['plumbing'] = [p.serialize() for p in Plumbing.query.all()]

    return json_as_configured(repr)

@app.route('/vessel/', methods=['GET', 'POST'])
def write_vessel():
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
