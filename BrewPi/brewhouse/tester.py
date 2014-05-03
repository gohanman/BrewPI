from BrewPi.data.database import db_session
from BrewPi.data.models import Recipes, Steps, Vessels, Pumps, Valves, Heaters, Coolers, Plumbing
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
            k1 = Vessels(
                vesselID=1, 
                name="HLT",
                currentVolume=0, 
                targetVolume=0,
                currentTemperature=0,
                targetTemperature=0,
                status = "OPEN",
                thermoDeviceFile="/dev/null",
                thermoDeviceDriver="testTemp",
                volumeDeviceFile="/dev/null",
                volumeDeviceDriver="testVol"
                )
            db_session.add(k1);

            k2 = Vessels(
                vesselID=2, 
                name="Mash",
                currentVolume=0, 
                targetVolume=0,
                currentTemperature=0,
                targetTemperature=0,
                status = "OPEN",
                thermoDeviceFile="/dev/null",
                thermoDeviceDriver="testTemp",
                volumeDeviceFile="/dev/null",
                volumeDeviceDriver="testVol"
                )
            db_session.add(k2);

            k3 = Vessels(
                vesselID=3, 
                name="Boil",
                currentVolume=0, 
                targetVolume=0,
                currentTemperature=0,
                targetTemperature=0,
                status = "OPEN",
                thermoDeviceFile="/dev/null",
                thermoDeviceDriver="testTemp",
                volumeDeviceFile="/dev/null",
                volumeDeviceDriver="testVol"
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

        from BrewPi.brewhouse.sensors import temperature, volume
        my_sensors = {} 
        my_volume = {}
        # initialize sensors from model definition
        for v in Vessels.query.all():
            class_name = v.thermoDeviceDriver
            obj = getattr(temperature, class_name)
            my_sensors[v.vesselID] = obj(v.thermoDeviceFile)
            v.currentTemperature = my_sensors[v.vesselID].read()

            class_name = v.volumeDeviceDriver
            obj = getattr(volume, class_name)
            my_volume[v.vesselID] = obj(v.volumeDeviceFile)
            v.currentVolume = my_volume[v.vesselID].read()

            db_session.commit()

        while not(self.stop.is_set()):

            for v,s in my_sensors.iteritems():
                next = s.read()
                Vessels.query.get(v).currentTemperature=next
                print str(v) + ":T" + str(next)

            for v,s in my_volume.iteritems():
                next = s.read()
                Vessels.query.get(v).currentVolume=next
                print str(v) + ":V" + str(next)

            db_session.commit()
            self.stop.wait(5)

        print "Tester Exiting"
