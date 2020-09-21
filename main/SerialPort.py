##############################################################################
'''                                  IMPORT                                '''
##############################################################################
import serial
import config
import WhatsappFuncs

# variabel objek serialport
global SerialPort

# fungsi delay
from time import sleep

##############################################################################
'''                              FUNGSI-FUNGSI                             '''
##############################################################################

def init_serial():
    global SerialPort
    ''' # Alternatif #1 : properti dipisah dari deklarasi objek
    SerialPort = serial.Serial()
    SerialPort.baudrate = 9600
    # windows
    SerialPort.port = 'COM3'
    # linux
    #SerialPort.port = '/dev/ttyUSB0'

    SerialPort.timeout = 10
    SerialPort.open()
    '''
    
    ''' # Alternatif #2 : properti di dalam deklarasi objek
    SerialPort = serial.Serial('COM3', 9600, timeout=1)
    '''
    SerialPort = serial.Serial(config.SERIAL_COM_PORT,config.SERIAL_BAUD_RATE, timeout=config.SERIAL_TIMEOUT)

    if SerialPort.isOpen():
        print('Serial Port Open Success @ ' + SerialPort.portstr)
    else:
        print('ERROR : Serial Port Open Failed!')

def start_SMS_reader():
    sleep(3)
    MsgFlag = False
    MsgAvailable = False
    MsgBuffer = []

    SerialPort.write(b'AT\r')
    SerialPort.write(b'AT+CMGF=1')
    SerialPort.write(b'\r')
    SerialPort.write(b'AT+CNMI=1,2,0,0,0')
    SerialPort.write(b'\r')
    
    while True:
        SerialIn = SerialPort.readline()
        
        # jika modul GSM mencetak sesuatu ke serial...
        if (SerialIn != b'') and (MsgFlag is True): # b'' artinya karakter kosong, diubah ke binary
            MsgBuffer.append(SerialIn)

        # jika ada pesan masuk (ada flag +CMT di 1 iterasi sblm nya)...
        if b'+CMT' in SerialIn or b'\r' not in SerialIn :
            MsgFlag = True
        else:
            MsgFlag = False
            MsgAvailable = True
        
        # jika pesan selesai direkam (sampai ketemu '\r\n')
        if MsgAvailable is True:
            if MsgBuffer != [b'\r\n'] and MsgBuffer != []:
                # keluarkan variabel nya di titik ini
                WhatsappFuncs.SendBufferToWA(config.PHONE_NUMBER,MsgBuffer)
                #print(MsgBuffer)
            # karena akan dikosongkan setelah itu dgn perintah ini
            MsgBuffer = []
            MsgAvailable = False
            
            