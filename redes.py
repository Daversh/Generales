import serial
import  serial.rs485
import threading as th

puerto = serial.Serial(port='COM3', baudrate=38400, stopbits=serial.STOPBITS_ONE)
ID = 2
name = "Dilan0"
Arch = open("Texto.txt", "r")
datAr = Arch.read()
datAr = datAr.replace("\n", "~")


def leer():
    while 1:
        data = puerto.read()
        print(data)

        '''
        if data[len(data) - 3] == (48 + ID) or data[len(data) - 3] == 48:
            msg = str(data)
            msg = msg.replace("~", "\n")
            print(msg[0:(len(msg) - 7)])
        if data[len(data) - 3] == (48 + ID) and data[len(data) - 4] == 65:
            direc = str(data[0] - 48)
            text_msg = str(ID) + "." + name + ": Archivo enviado:~" + datAr + direc + "\r\n"
            print(text_msg)
            Ascii = text_msg.encode("utf-8")
            puerto.write(Ascii)
            '''


Hilo = th.Thread(target=leer)
Hilo.start()

puerto.write([7])
msg = [255, 1, 0, 10, 20, 15, 16]
puerto.write(int(500).to_bytes(4, "big"))
'''
while 1:
    text = input()
    text = str(ID) + "." + name + ": " + text + "\r\n"
    ascii_values = text.encode("utf-8")
    puerto.write(ascii_values)
'''