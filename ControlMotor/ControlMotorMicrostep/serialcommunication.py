import serial, time
from serial.tools import list_ports


# Look what there are in the serial ports
ports = list_ports.comports()

for item in ports:
    print(item.name, ':', item.description)

# Open the serial port for Arduino COM
port = ports[0].name
baud = 9600

try:
    ser = serial.Serial(port, baud) # open the serial port
except serial.SerialException as var: # var contains details of the issue
    print('An exception occured')
    print('Exception details', var)
else:
    print('Serial port ' + port + ' opened.')
    
    time.sleep(1) # We have to wait some time before send anything to the Arduino
    ser.write(b'POSITION:2000\n')
    print('- Send: ')   
    ser.close()
    print('Closed PORT')
