class volume:

    def __init__(self, device_file):
        pass

    def read(self):
        return None

class testVol(volume):

    my_vol = 0

    def __init__(self, device_file):
        import random
        self.my_vol = random.randrange(4, 4*20, 1)

    def read(self):
        import random
        step = random.randrange(-1, 1, 1)
        self.my_vol += step

        return self.my_vol
