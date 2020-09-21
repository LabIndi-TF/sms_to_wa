##############################################################################
'''                                  IMPORT                                '''
##############################################################################

##############################################################################
'''                                INISIASI                                '''
##############################################################################
global SERIAL_COM_PORT, SERIAL_BAUD_RATE, SERIAL_TIMEOUT
global PHONE_NUMBER
global TEXT_ENCODING

##############################################################################
'''                             DEFINISI KELAS                             '''
##############################################################################
def init_config():
    global SERIAL_COM_PORT, SERIAL_BAUD_RATE, SERIAL_TIMEOUT
    global PHONE_NUMBER
    global TEXT_ENCODING

    SERIAL_COM_PORT = 'COM3'
    SERIAL_BAUD_RATE = 9600;
    SERIAL_TIMEOUT = 10;

    PHONE_NUMBER = '6281220587597'

    TEXT_ENCODING = 'utf-8'