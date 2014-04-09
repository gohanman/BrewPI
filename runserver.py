from BrewPi.web.app import WebProcess
from BrewPi.brewhouse.tester import TestingBackend
from multiprocessing import Pipe

p1, p2 = Pipe()
backend = TestingBackend()
backend.assignWebServer(p1)
backend.daemon = True
frontend = WebProcess()
frontend.assignToBrewhouse(p2)
frontend.daemon = True

frontend.start()
backend.start()

from time import sleep
while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        backend.stop.set()
        backend.join()
        break
