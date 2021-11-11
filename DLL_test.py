import ctypes
from ctypes import windll
from time import sleep

if __name__ == '__main__':

    # load DLL
    mydll = windll.LoadLibrary("MEGSV4x64.dll")

    # measuring value variable
    out1 = ctypes.c_double(0)
    out2 = ctypes.c_double(0)
    out3 = ctypes.c_double(0)
    out4 = ctypes.c_double(0)

    # pointer tomeasuring value variable
    p_out1 = ctypes.pointer(out1)
    p_out2 = ctypes.pointer(out2)
    p_out3 = ctypes.pointer(out3)
    p_out4 = ctypes.pointer(out4)

    Comnr = ctypes.c_int(14)        # COM port
    Baud = ctypes.c_int(115200)     # baud rate
    BufSize = ctypes.c_int(2048)    # buffer size

    # channel numbers
    chan1 = ctypes.c_int(1)
    chan2 = ctypes.c_int(2)
    chan3 = ctypes.c_int(3)
    chan4 = ctypes.c_int(4)

    # open COM port
    ErrCode1 = mydll.GSV4actExt(Comnr, Baud, BufSize)

    # start transmission of measuring values
    ErrCode2 = mydll.GSV4startTX(Comnr)

    sleep(1)

    print("number of measuring values in buffer: ",  mydll.GSV4received(Comnr, chan1), mydll.GSV4received(Comnr, chan2),
                                                     mydll.GSV4received(Comnr, chan3), mydll.GSV4received(Comnr, chan4))
    OutputStatus1 = mydll.GSV4read(Comnr, chan1, p_out1)
    OutputStatus2 = mydll.GSV4read(Comnr, chan2, p_out2)
    OutputStatus3 = mydll.GSV4read(Comnr, chan3, p_out3)
    OutputStatus4 = mydll.GSV4read(Comnr, chan4, p_out4)
    print("Output of Channel 1 is: " + str(out1.value))
    print("Output of Channel 2 is: " + str(out2.value))
    print("Output of Channel 3 is: " + str(out3.value))
    print("Output of Channel 4 is: " + str(out4.value))

    # stop transmission of measuring values
    ErrCode3 = mydll.GSV4stopTX(Comnr)

    # close COM port
    ErrCode4 = mydll.GSV4release(Comnr)
