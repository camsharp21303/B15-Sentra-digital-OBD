import obd
import time
from obd import commands

PORT = "/dev/ttyUSB0"

data = [
    commands.RPM,
    commands.SPEED,
    commands.COOLANT_TEMP,
    commands.ENGINE_LOAD
]

class car:
    def __init__(self, port):
        self.connection = obd.Async(port)
        for i in data:
            self.connection.watch(i)

        
        self.connection.start()
        time.sleep(3)


    def getData(self):
        results = dict()
        if(commands.SPEED in data):
            response = self.connection.query(commands.SPEED)
            results["speed"] = response.value.to("mph").magnitude // 1
        if(commands.RPM in data):
            response = self.connection.query(commands.RPM)
            results["rpm"] = response.value.magnitude
        if(commands.COOLANT_TEMP in data):
            response = self.connection.query(commands.COOLANT_TEMP)
            results["coolant"] = response.value.to('fahrenheit').magnitude // 1
        if(commands.ENGINE_LOAD in data):
            response = self.connection.query(commands.ENGINE_LOAD)
            results["load"] = response.value.magnitude
        return results
        
