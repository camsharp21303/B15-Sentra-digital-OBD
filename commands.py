import obd

c = obd.OBD("/dev/ttyUSB0")

for i in c.supported_commands:
    print(i)