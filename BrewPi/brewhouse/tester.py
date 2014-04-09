from BrewPi.data.database import db_session
from BrewPi.data.models import Recipes, Steps, Kettles
from threading import Event
from multiprocessing import Process, Pipe

class TestingBackend(Process):

    def __init__(self):
        Process.__init__(self)
        self.stop = Event()

    def assignWebServer(self, p):
        self.web_pipe = p

    def run(self):
        import os
        print "Backend PID: " + str(os.getpid())
        print "Initializing Data"
        try:
            k1 = Kettles(
                kettleID=1, 
                name="HLT",
                currentVolume=0, 
                targetVolume=0,
                currentTemperature=0,
                targetTemperature=0,
                status = "OPEN"
                )
            db_session.add(k1);

            k2 = Kettles(
                kettleID=2, 
                name="Mash",
                currentVolume=0, 
                targetVolume=0,
                currentTemperature=0,
                targetTemperature=0,
                status = "OPEN"
                )
            db_session.add(k2);

            k3 = Kettles(
                kettleID=3, 
                name="Boil",
                currentVolume=0, 
                targetVolume=0,
                currentTemperature=0,
                targetTemperature=0,
                status = "OPEN"
                )
            db_session.add(k3);

            db_session.commit()
        except:
            # records probably exist; that's fine
            db_session.rollback()

        try:
            s1 = Steps(
                    stepID=1,
                    startTimestamp=1396899784,
                    targetDuration=200,
                    endTimestamp=1396899984,
                    status='Heating'
                )
            db_session.add(s1)
            print "create step"
            db_session.commit()
        except:
            # records probably exist; that's fine
            db_session.rollback()

        try:
            r1 = Recipes(
                    recipeID=1,
                    startTimestamp=1396899784,
                    targetDuration=200,
                    endTimestamp=1396899984,
                    status='Brewing',
                    currentStepID=1
                )
            db_session.add(r1)
            db_session.commit()
        except:
            # records probably exist; that's fine
            db_session.rollback()

        while not(self.stop.is_set()):
            self.stop.wait(5)

        print "Tester Exiting"
