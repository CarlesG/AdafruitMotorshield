import serial, time
from serial.tools import list_ports


# Look what there are in the serial ports
ports = list_ports.comports()
print("---------------------------------------------")
for item in ports:
    print(item.name, ':', item.description)
print("---------------------------------------------")
port = ports[0].name
baud = 9600

try:
# Open the serial port for Arduino COM
    ser = serial.Serial(port, baud, timeout = 2) 
except serial.SerialException as var: # var contains details of the issue
    print('An exception occured')
    print('Exception details', var)
else:
    print('Serial port ' + port + ' opened.')
    time.sleep(1) # We have to wait some time before send anything to the Arduino
    try:
        ser.write(b'POSITION2:200\r\n') # carry return and newline
        ser.write(b'POSITION2?\r\n') # carry return and newline
        msg = ser.readline().decode("utf-8")
        #print(msg)
        msg = msg.removesuffix('\r\n')
        print('Posición leida: ',msg)
    except serial.SerialException as var2:
        print('An exception occured')
        print('Exception details', var2)
    else:
        ser.close()
        print('Closed PORT')



def escribir_posicion():
    
    pass

def leer_posicion():
    pass

