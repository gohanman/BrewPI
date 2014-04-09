from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base

# A physical vessel
class Kettles(Base):
    __tablename__ = 'Kettles'

    kettleID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    currentVolume = Column(Numeric(10,3))
    targetVolume = Column(Numeric(10,3))
    currentTemperature = Column(Numeric(10,3))
    targetTemperature = Column(Numeric(10,3))
    status = Column(String(10))

    def __repr__(self):
        return '<Kettle %r>' % (self.kettleID)

    def serialize(self):
        repr = {}
        repr['kettleID'] = self.kettleID
        repr['name'] = self.name
        repr['currentVolume'] = str(self.currentVolume)
        repr['targetVolume'] = str(self.targetVolume)
        repr['currentTemperature'] = str(self.currentTemperature)
        repr['targetTemperature'] = str(self.targetTemperature)
        repr['status'] = self.status
        return repr

# A discrete step of a brew (mash, boil, etc)
class Steps(Base):
    __tablename__ = 'Steps'

    stepID = Column(Integer, primary_key=True, autoincrement=True)
    startTimestamp = Column(Integer)
    targetDuration = Column(Integer)
    endTimestamp = Column(Integer)
    status = Column(String(100))

    def serialize(self):
        repr = {}
        repr['stepID'] = self.stepID
        repr['startTimestamp'] = str(self.startTimestamp)
        repr['targetDuration'] = str(self.targetDuration)
        repr['endTimestamp'] = str(self.endTimestamp)
        repr['status'] = str(self.status)
        return repr

# A collection of steps for a complete brew
class Recipes(Base):
    __tablename__ = 'Recipes'

    recipeID = Column(Integer, primary_key=True, autoincrement=True)
    startTimestamp = Column(Integer)
    targetDuration = Column(Integer)
    endTimestamp = Column(Integer)
    status = Column(String(100))
    currentStepID = Column(Integer)

    def serialize(self):
        repr = {}
        repr['receipeID'] = self.recipeID
        repr['startTimestamp'] = str(self.startTimestamp)
        repr['targetDuration'] = str(self.targetDuration)
        repr['endTimestamp'] = str(self.endTimestamp)
        repr['status'] = str(self.status)
        return repr

# list of steps for a given recipe
class RecipeStepMap(Base):
    __tablename__ = 'RecipeStepMap'

    recipeStepMapID = Column(Integer, primary_key=True, autoincrement=True)
    recipeID = Column(Integer)
    stepID = Column(Integer)

# list of step dependencies
class StepMap(Base):
    __tablename__ = 'StepMap'

    stepMapID = Column(Integer, primary_key=True, autoincrement=True)
    stepID = Column(Integer)
    dependencyID = Column(Integer)
