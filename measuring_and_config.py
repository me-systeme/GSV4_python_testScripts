import serial, struct
from time import sleep

def printFrameHex(data):
    print(' '.join(f'{c:0>2X}' for c in data))

def rcvMeasVals(ser):
    MeasValues = []
    p = ser.read(1)
    if len(p)>0 and p[0] == 0xA5:
        data = ser.read(10)
        if data[8] == 0x0D and data[9] == 0x0A:
            #MeasValues = struct.unpack(">hhhh", data[:8])
            for i in range(4):
                val = ((data[0] * 256 + data[1]) - 32768) / 32768
                MeasValues.append(val)
    return MeasValues


def buildFrame(cmd, data):
    print(cmd, data)

def start_transmision(ser):
    ser.write(b'\x24')

def stop_transmision(ser):
    ser.write(b'\x23')
    sleep(0.1)
    ser.reset_input_buffer()

def get_firmware_version(ser):
    stop_transmision(ser)
    ser.write(b'\x2b')
    data = ser.read(11)
    fw_version = data[8]
    print(f"Firmware-Version: {fw_version}")
    return fw_version

def set_zero(ser, channel):
    stop_transmision(ser)
    ser.write(b'\x0C' + channel.to_bytes(1,'big'))

def get_serial_number(ser):
    stop_transmision(ser)
    ser.write(b'\x1F')
    data = ser.read(18)
    serno = data[8:16].decode("utf-8")
    print(f"Seriennummer: {serno}")
    return serno

def get_frequency(ser):
    datarates = {
        0xA0: 0.625,
        0xA1: 1.250,
        0xA2: 2.500,
        0xA3: 3.750,
        0xA4: 6.250,
        0xA5: 7.500,
        0xA6: 12.40,
        0xA7: 14.70,
        0xA8: 24.40,
        0xA9: 125.0,
        0xAA: 250.0,
        0xAB: 500.0,
        0xAC: 937.5,
    }
    stop_transmision(ser)
    ser.write(b'\x16')
    data = ser.read(11)
    datarate = data[8]
    if datarate in datarates.keys():
        print(f"Datenfrequenz: {datarates[datarate]} Messwerte/Sekunde")
    else:
        print(f"Fehler beim Lesen der Datenfrequenz: {datarate:0>2X}")

def get_value(ser):
    ser.reset_input_buffer()
    ser.write(b'\x3b')
    return rcvMeasVals(ser)

def unlock_config(ser):
    ser.write(b'\x26\x01\x62\x65\x72\x6C\x69\x6E')

def lock_config(ser):
    ser.write(b'\x26\x00\x62\x65\x72\x6C\x69\x6E')

if __name__ == '__main__':

    ser = serial.Serial(port='COM13', baudrate=115200, timeout=1)
    ser.reset_input_buffer()

    get_firmware_version(ser)
    unlock_config(ser)
    get_serial_number(ser)
    get_frequency(ser)
    start_transmision(ser)
    lock_config(ser)

    for i in range(10):
        MeasValues = get_value(ser)
        print(MeasValues)
        sleep(0.1)

    unlock_config(ser)
    set_zero(ser, channel=1)
    start_transmision(ser)
    lock_config(ser)
    ser.reset_input_buffer()

    for i in range(10):
        MeasValues = rcvMeasVals(ser)
        print(MeasValues)
    ser.close()
