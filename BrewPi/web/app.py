from flask import Flask
app = Flask(__name__)
from multiprocessing import Process, Pipe

import BrewPi.web.views

class WebProcess(Process):

    def assignToBrewhouse(self, p):
        self.brewhouse_pipe = p

    def run(self):
        import os
        print "Frontend PID: " + str(os.getpid())
        app.run(host='0.0.0.0',debug=False)
