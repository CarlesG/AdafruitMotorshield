import serial, time
from serial.tools import list_ports
import numpy as np

''' This is script is for implement the module functions for the use in control
two motors at the same time with one Arduino via RS-232 protocol. See the README.md
for mor details about the Arduino implementation or directly in ControlMotorSingle.ino 
or ControlMotorMicrostep.ino
'''
# -------------------------------------------------
# TEST MAIN
# -------------------------------------------------

def main():
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
        ser = serial.Serial(port, baud, timeout = 3) 
    except serial.SerialException as var: # var contains details of the issue
        print('An exception occured')
        print('Exception details', var)
    else:
        print('Serial port ' + port + ' opened.')
        time.sleep(3) # We have to wait some time before send anything to the Arduino
        try:
        # Testing position function. 
            write_position(ser, 100, 2)
            while(int(read_position(ser, 2)) != 100):
                print(read_position(ser, 2))
        # Testing  go to reset function 
            gotoreset(ser, 2) 
            ser.flush()
            print(read_position(ser, 2))
            
        except serial.SerialException as var2:
            print('An exception occured')
            print('Exception details', var2)
        else:
            pass

# --------------------------------------------------
#           FUNCTIONS IMPLEMENTATION
# --------------------------------------------------

def write_position(serial, position, select_motor):
    ''' Write the desired position in serial port for motor 2

    Parameters
    ----------
    * serial: serial class
    * position: int value
        desired position that we want to move the motor 2
    * select_motor: int value
        motor to control. It can be 1 (M1 and M2 connection),2 (M3 and M4 connection) or both
    
    Returns
    -------
    None
    '''
    serial.reset_output_buffer()
    serial.reset_input_buffer()

    if select_motor == 2:
        serial.write(bytes('POSITION2:' + str(position) + '\r\n','utf-8'))
    elif select_motor == 1:
        serial.write(bytes('POSITION1:' + str(position) + '\r\n','utf-8'))
    elif select_motor == 0:
        serial.write(bytes('POSITION:' + str(position) + '\r\n','utf-8'))

def read_position(serial, select_motor):
    ''' Read the position on the serial port 

    Parameters
    ----------
    * serial: serial class
    * select_motor: int 
        motor to read the position. It can be 1 (M1 and M2 connection) or 2 (M3 and M4 connection) or both

    Returns
    -------
    None
    '''
    if select_motor == 2:
        serial.write(bytes('POSITION2?\r\n','utf-8'))
    elif select_motor == 1:
        serial.write(bytes('POSITION1?\r\n','utf-8'))
    elif select_motor == 0:
        serial.write(bytes('POSITION?\r\n','utf-8'))
    msg = serial.readline().decode("utf-8")
    msg = msg.removesuffix('\r\n')
    return msg

def gotoreset(serial, motor):
    ''' Read the position on the serial port 
    
    Parameters
    ----------
    * serial 

    Returns
    -------
    None
    '''
    serial.reset_output_buffer()
    serial.reset_input_buffer()

    if motor == 2:
        serial.write(bytes('GOTORESET2\r\n','utf-8'))
    elif motor == 1:
        serial.write(bytes('GOTORESET1\r\n','utf-8'))
    elif motor == 0:
        serial.write(bytes('GOTORESET\r\n','utf-8')) 
    else:
        print('Not valid parameter')
        return

    while(read_position(serial) == ""):
        pass
    print('I have finished the reset')

if __name__ == "__main__":
    main()
