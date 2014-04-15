from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from database import Base

# A physical vessel
class Vessels(Base):
    __tablename__ = 'Vessels'

    vesselID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    currentVolume = Column(Numeric(10,3))
    targetVolume = Column(Numeric(10,3))
    maxVolume = Column(Numeric(10,3))
    deadSpace = Column(Numeric(10,3))
    currentTemperature = Column(Numeric(10,3))
    targetTemperature = Column(Numeric(10,3))
    boilOff = Column(Numeric(10,3))
    status = Column(String(10))
    fired = Column(Integer)
    heaterID = Column(Integer, ForeignKey('Heaters.heaterID'))
    positionX = Column(Integer)
    positionY = Column(Integer)

    def __repr__(self):
        return '<Vessel %r>' % (self.vesselID)

    def serialize(self):
        repr = {}
        repr['vesselID'] = self.vesselID
        repr['name'] = self.name
        repr['volume'] = {}
        repr['volume']['currentVolume'] = str(self.currentVolume)
        repr['volume']['targetVolume'] = str(self.targetVolume)
        repr['volume']['maxVolume'] = str(self.maxVolume)
        repr['volume']['deadSpace'] = str(self.deadSpace)
        repr['currentTemperature'] = str(self.currentTemperature)
        repr['targetTemperature'] = str(self.targetTemperature)
        repr['boilOff'] = str(self.boilOff)
        repr['status'] = str(self.status)
        repr['fired'] = str(self.fired)
        repr['heaterID'] = { 'heat_input' : str(self.heaterID) }
        repr['position'] = { 'left' : str(self.positionX), 'top' : str(self.positionY) }

        return repr

class Pumps(Base):
    __tablename__ = 'Pumps'

    pumpID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(100))
    active = Column(Integer)
    positionX = Column(Integer)
    positionY = Column(Integer)

    def serialize(self):
        repr = {}
        repr['pumpID'] = self.pumpID
        repr['name'] = self.name
        repr['description'] = self.description
        repr['active'] = str(self.active)
        repr['position'] = { 'left' : str(self.positionX), 'top' : str(self.positionY) }

        return repr

class Valves(Base):
    __tablename__ = 'Valves'

    valveID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(100))
    type = Column(Integer)
    active = Column(Integer)
    direction = Column(String(10))
    manual = Column(Integer)
    positionX = Column(Integer)
    positionY = Column(Integer)

    def serialize(self):
        repr = {}
        repr['valveID'] = self.valveID
        repr['name'] = self.name
        repr['description'] = self.description
        repr['type'] = str(self.type)
        repr['active'] = str(self.active)
        repr['direction'] = self.direction
        repr['manual'] = str(self.manual)
        repr['position'] = { 'left' : str(self.positionX), 'top' : str(self.positionY) }

        return repr

class Heaters(Base):
    __tablename__ = 'Heaters'

    heaterID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(100))
    active = Column(Integer)
    positionX = Column(Integer)
    positionY = Column(Integer)

    def serialize(self):
        repr = {}
        repr['heaterID'] = self.heaterID
        repr['name'] = self.name
        repr['description'] = self.description
        repr['active'] = str(self.active)
        repr['position'] = { 'left' : str(self.positionX), 'top' : str(self.positionY) }

        return repr

class Coolers(Base):
    __tablename__ = 'Coolers'

    coolerID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(100))
    active = Column(Integer)
    positionX = Column(Integer)
    positionY = Column(Integer)

    def serialize(self):
        repr = {}
        repr['coolerID'] = self.coolerID
        repr['name'] = self.name
        repr['description'] = self.description
        repr['active'] = str(self.active)
        repr['position'] = { 'left' : str(self.positionX), 'top' : str(self.positionY) }

        return repr

class Plumbing(Base):
    __tablename__ = 'Plumbing'

    plumbingID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(100))
    label = Column(String(100))
    active = Column(Integer)

    points = relationship('PlumbingPoints', backref='plumbing')

    def serialize(self):
        repr = {}
        repr['plumbingID'] = self.plumbingID
        repr['name'] = self.name
        repr['description'] = self.description
        repr['label'] = self.label
        repr['active'] = str(self.active)
        repr['points'] = [p.serialize() for p in self.points]

        return repr

# list of points associated with a given plumbing line
class PlumbingPoints(Base):
    __tablename__ = 'PlumbingPoints'

    plumbingPointID = Column(Integer, primary_key=True, autoincrement=True)
    plumbingID = Column(Integer, ForeignKey('Plumbing.plumbingID'))
    positionX = Column(Integer)
    positionY = Column(Integer)

    def serialize(self):
        repr = { 'x' : self.positionX, 'y' : self.positionY }

        return repr

# many-to-many mapping tables
step_vessel_map = Table('StepVesselMap', Base.metadata,
                        Column('stepID', ForeignKey('Steps.stepID')),
                        Column('vesselID', ForeignKey('Vessels.vesselID'))
                  )

step_pump_map = Table('StepPumpMap', Base.metadata,
                        Column('stepID', ForeignKey('Steps.stepID')),
                        Column('pumpID', ForeignKey('Pumps.pumpID'))
                  )

step_valve_map = Table('StepValveMap', Base.metadata,
                        Column('stepID', ForeignKey('Steps.stepID')),
                        Column('valveID', ForeignKey('Valves.valveID'))
                  )

step_heater_map = Table('StepHeaterMap', Base.metadata,
                        Column('stepID', ForeignKey('Steps.stepID')),
                        Column('heaterID', ForeignKey('Heaters.heaterID'))
                  )

step_cooler_map = Table('StepCoolerMap', Base.metadata,
                        Column('stepID', ForeignKey('Steps.stepID')),
                        Column('coolerID', ForeignKey('Coolers.coolerID'))
                  )

# A discrete step of a brew (mash, boil, etc)
class Steps(Base):
    __tablename__ = 'Steps'

    stepID = Column(Integer, primary_key=True, autoincrement=True)
    startTimestamp = Column(Integer)
    targetDuration = Column(Integer)
    endTimestamp = Column(Integer)
    status = Column(String(100))

    vessels = relationship('Vessels', secondary=step_vessel_map, backref='steps')
    pumps = relationship('Pumps', secondary=step_pump_map, backref='steps')
    valves = relationship('Valves', secondary=step_valve_map, backref='steps')
    heaters = relationship('Heaters', secondary=step_heater_map, backref='steps')
    coolers = relationship('Coolers', secondary=step_cooler_map, backref='steps')

    def serialize(self):
        repr = {}
        repr['stepID'] = self.stepID
        repr['startTimestamp'] = str(self.startTimestamp)
        repr['targetDuration'] = str(self.targetDuration)
        repr['endTimestamp'] = str(self.endTimestamp)
        repr['status'] = str(self.status)
        repr['components'] = {}
        repr['components']['vessels'] = [v.name for v in self.vessels]
        repr['components']['pumps'] = [str(p.pumpID) for p in self.pumps]
        repr['components']['valves'] = [str(v.valveID) for v in self.valves]
        repr['components']['heaters'] = [str(h.heaterID) for h in self.heaters]
        repr['components']['coolers'] = [str(c.coolerID) for c in self.coolers]

        return repr

recipe_step_map = Table('RecipeStepMap', Base.metadata,
                        Column('recipeID', ForeignKey('Recipes.recipeID')),
                        Column('stepID', ForeignKey('Steps.stepID'))
                  )

# A collection of steps for a complete brew
class Recipes(Base):
    __tablename__ = 'Recipes'

    recipeID = Column(Integer, primary_key=True, autoincrement=True)
    startTimestamp = Column(Integer)
    targetDuration = Column(Integer)
    endTimestamp = Column(Integer)
    status = Column(String(100))
    currentStepID = Column(Integer)

    steps = relationship('Steps', secondary=recipe_step_map)

    def serialize(self):
        repr = {}
        repr['receipeID'] = self.recipeID
        repr['startTimestamp'] = str(self.startTimestamp)
        repr['targetDuration'] = str(self.targetDuration)
        repr['endTimestamp'] = str(self.endTimestamp)
        repr['status'] = str(self.status)
        repr['steps'] = [s.serialize() for s in self.steps]

        return repr

# list of step dependencies
class StepMap(Base):
    __tablename__ = 'StepMap'

    stepMapID = Column(Integer, primary_key=True, autoincrement=True)
    stepID = Column(Integer, ForeignKey('Steps.stepID'))
    dependencyID = Column(Integer, ForeignKey('Steps.stepID'))

