##############################################################################
'''                                  IMPORT                                '''
##############################################################################
import serial

# variabel objek serialport
global SerialPort

# fungsi delay
from time import sleep

##############################################################################
'''                              FUNGSI-FUNGSI                             '''
##############################################################################

def InitSerial():
    global SerialPort
    '''
    SerialPort = serial.Serial()
    SerialPort.baudrate = 9600
    # windows
    SerialPort.port = 'COM3'
    # linux
    #SerialPort.port = '/dev/ttyUSB0'

    SerialPort.timeout = 10
    SerialPort.open()
    '''

    SerialPort = serial.Serial('COM3', 9600, timeout=1)

    if SerialPort.isOpen():
        print('Serial Port Open Success @ ' + SerialPort.portstr)

def StartSMSReader():
    sleep(3);
    SerialPort.write(b'AT\r');
    
    SerialPort.write(b'AT+CMGF=1');
    SerialPort.write(b'\r');
    SerialPort.write(b'AT+CNMI=1,2,0,0,0');
    SerialPort.write(b'\r');
    
    while True:
        SerialIn = SerialPort.readline()
        
        if SerialIn != b'': # b'' artinya karakter kosong, diubah ke binary
            print(SerialIn)
        
##############################################################################
'''                               MAIN LOOP                                '''
##############################################################################
InitSerial()
StartSMSReader()