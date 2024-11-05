

class memristor_circuit(object):
    def __init__(self, memristor, timeBegin, timeEnd):
        self.memristor = memristor
        self.timeBegin = timeBegin
        self.timeEnd = timeEnd



class create_memristor_circuit(object):

    def __init__(self, voltageFunction, memristor, time1, time2, samplingFrequency):
        self.voltageFunction = voltageFunction
        self.memristor = memristor
        self.memristor.calculate_fixed_parameters()
        self.time1 = time1
        self.time2 = time2
        self.samples = int(samplingFrequency * (self.time2 - self.time1))
        self.timeInstants = np.linspace(self.time1, self.time2, self.samples)



if __name__ == '__main__':
    pass