import obd
import time

com = "/dev/ttyUSB0"

connection = obd.OBD(com)

time.sleep(2)

for i in range(10):
    init = time.time()
    response = connection.query(obd.commands.SPEED)
    connection.query(obd.commands.RPM)
    print(time.time() - init)
