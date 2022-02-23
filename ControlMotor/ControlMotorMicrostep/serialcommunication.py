import serial, time
from serial.tools import list_ports

def escribir_posicion(serial,posicion):
    serial.write(bytes('POSITION2:' + str(posicion) + '\r\n','utf-8'))

def leer_posicion(serial):
    serial.write(bytes('POSITION2?\r\n','utf-8'))
    msg = serial.readline().decode("utf-8")
    msg = msg.removesuffix('\r\n')
    print(msg)
    return int(msg)

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
        escribir_posicion(ser, 200)
        msg = leer_posicion(ser)
        print('Posición leida: ',msg)
    except serial.SerialException as var2:
        print('An exception occured')
        print('Exception details', var2)
    else:
        ser.close()
        print('Closed PORT')