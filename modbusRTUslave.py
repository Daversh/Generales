import serial
import threading as th

puerto = serial.Serial(port='COM3', baudrate=38400)
ID = 1006867427
Address = 0x01
Reg1 = 0x0f0f
Reg2 = 0xf0f0
coil1 = 0b0
coil2 = 0b1

def CRC_MOD16(data):
    CRC = 0xffff
    poly = 0xA001
    for i in data:
        CRC ^= i
        for j in range(8):
            if (CRC & 0x0001) != 0:
                CRC >>= 1
                CRC ^= poly
            else:
                CRC >>= 1
    print(hex(CRC))
    return CRC

while 1:
    data = puerto.readline()
    detEr = CRC_MOD16(data[0:(len(data) - 2)])
    print(detEr)
    '''if fn == 1:                   #Reald coils
    elif fn == 3:                 #Read holding registers

    elif fn == 5:                 #write single coil

    elif fn == 6:                 #write single register

    elif fn == 15:                #write multiple coils

    elif fn == 16:                #write multiple registers

    elif fn == 23:                #read/write multiple registers

    else:
        exCode=1'''