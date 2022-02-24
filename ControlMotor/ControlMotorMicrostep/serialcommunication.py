import serial, time
from serial.tools import list_ports
import numpy as np

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
        
            write_position(ser,100)
            while(int(read_position(ser)) != 100):
                print(read_position(ser))
        # Testing  go to reset function 
            gotoreset(ser) 
            ser.flush()
            print(read_position(ser))
            
        except serial.SerialException as var2:
            print('An exception occured')
            print('Exception details', var2)
        else:
            pass


def write_position(serial,position):
    ''' Write the desired position in serial port for motor 2

    Parameters
    ----------
    * serial: serial class
    * position: int value
        desired position that we want to move the motor 2
    
    Returns
    -------
    None
    '''
    serial.reset_output_buffer()
    serial.reset_input_buffer()
    serial.write(bytes('POSITION2:' + str(position) + '\r\n','utf-8'))

def read_position(serial):
    ''' Read the position on the serial port 

    Parameters
    ----------
    * serial: serial class

    Returns
    -------
    None
    '''
    serial.write(bytes('POSITION2?\r\n','utf-8'))
    msg = serial.readline().decode("utf-8")
    msg = msg.removesuffix('\r\n')
    return msg

def gotoreset(serial):
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
    serial.write(bytes('GOTORESET2\r\n','utf-8'))
    while(read_position(serial) == ""):
        pass
    print('I have finished the reset')
   
if __name__ == "__main__":
    main()