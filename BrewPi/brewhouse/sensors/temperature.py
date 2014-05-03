class temperature:

    def __init__(self, device_file):
        pass

    def read(self):
        return None

class testTemp(temperature):

    my_temp = 0

    def __init__(self, device_file):
        import random
        self.my_temp = random.randrange(70, 212, 1)

    def read(self):
        import random
        step = random.randrange(-1, 1, 1)
        self.my_temp += step

        return self.my_temp
