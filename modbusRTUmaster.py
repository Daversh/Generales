import serial
import threading as th

puerto = serial.Serial(port='COM3', baudrate=38400)

def Bar2Int(ar):
    IntAr = []
    for B_it in ar:
        IntAr.append(int.from_bytes(B_it, "big"))
    return IntAr

def leer():
    while 1:
        data = [puerto.read(1)]
        while puerto.inWaiting() > 0:
            data.append(puerto.read(1))
        dataN = Bar2Int(data)
        print("\n", data)
        print(dataN)

def CRC_MOD16(dataIn):
    CRC = 0xffff
    poly = 0xA001
    for i in dataIn:
        CRC ^= i
        for j in range(8):
            if (CRC & 0x0001) != 0:
                CRC >>= 1
                CRC ^= poly
            else:
                CRC >>= 1
    CRCOUT = (CRC // 256) + ((CRC % 256) * 256)
    return CRCOUT

def NUM16(n16):
    return [n16//256, n16%256]


mode = int(input("[0]Master [1]Slave: "))
if mode == 0:
    ID = 1006867427
    Address = 0x00

    Hilo = th.Thread(target=leer)
    Hilo.start()

    while 1:
        ad = int(input("direccion de solicitud en decimal: "))
        fn = int(input("Funcion de solicitud en decimal: "))
        msg = []
        N = 0
        N0 = 0
        N1 = 0
        N2 = 0
        N3 = 0
        if fn == 1:  # Reald coils      adx8/fnx8/n0x16/n1x16/crcx16
            N0 = int(input("direccion de bobina inicial a leer: "))
            N1 = int(input("numero de bobinas a leer: "))
            msg.extend([ad, fn])
            msg.extend(NUM16(N0))
            msg.extend(NUM16(N1))
        elif fn == 3:  # Read holding registers        adx8/fnx8/n0x16/n1x16/crcx16
            N0 = int(input("direccion del registro inicial a leer: "))
            N1 = int(input("numero de registros a leer: "))
            msg.extend([ad, fn])
            msg.extend(NUM16(N0))
            msg.extend(NUM16(N1))

        elif fn == 5:  # write single coil            adx8/fnx8/n0x16/n1x16/crcx16
            N0 = int(input("direccion de la bobina a escribir: "))
            N1 = int(input("estado binario a escribir: "))
            if N1 == 1:
                N1 = 0xFF00
            msg.extend([ad, fn])
            msg.extend(NUM16(N0))
            msg.extend(NUM16(N1))

        elif fn == 6:  # write single register        adx8/fnx8/n0x16/n1x16/crcx16
            N0 = int(input("direccion del registro a escribir: "))
            N1 = int(input("numero a escribir en decimal: "))
            msg.extend([ad, fn])
            msg.extend(NUM16(N0))
            msg.extend(NUM16(N1))

        elif fn == 15:  # write multiple coils         adx8/fnx8/n0x16/n1x16/Nx8/N*x8/crcx16
            N0 = int(input("direccion de bobina inicial a escribir: "))
            N1 = int(input("numero de bobinas a escribir: "))
            if N1 % 8 == 0:
                N = N1 / 8
            else:
                N = (N1 // 8) + 1
            msg.extend([ad, fn])
            msg.extend(NUM16(N0))
            msg.extend(NUM16(N1))
            msg.append(N)
            coilB = 0
            ci = 0
            for i in range(N1):
                coilB += int(input("estado de la bobina " + str(N0 + i) + ": ")) * pow(2, ci)
                ci += 1
                if ci == 8 or i == (N1 - 1):
                    ci = 0
                    msg.append(coilB)
                    coilB = 0

        elif fn == 16:  # write multiple registers         adx8/fnx8/n0x16/n1x16/N/N*2*x8/crcx16
            N0 = int(input("direccion de registro inicial a escribir: "))
            N1 = int(input("numero de registros a escribir: "))
            N = 2 * N1
            msg.extend([ad, fn])
            msg.extend(NUM16(N0))
            msg.extend(NUM16(N1))
            msg.append(N)
            for i in range(N1):
                msg.extend(NUM16(int(input("numero para el registro " + str(N0 + i) + ": "))))

        elif fn == 23:  # read/write multiple registers    adx8/fnx8/n0x16/n1x16/n2x16/n3x16/N/n4xN/crcx16
            N0 = int(input("direccion del registro inicial a leer: "))
            N1 = int(input("numero de registros a leer: "))
            N2 = int(input("direccion de registro inicial a escribir: "))
            N3 = int(input("numero de registros a escribir: "))
            N = 2 * N3
            msg.extend([ad, fn])
            msg.extend(NUM16(N0))
            msg.extend(NUM16(N1))
            msg.extend(NUM16(N2))
            msg.extend(NUM16(N3))
            msg.append(N)
            for i in range(N3):
                msg.extend(NUM16(int(input("numero para el registro " + str(N2 + i) + ": "))))

        crcNum = CRC_MOD16(msg)
        msg.extend(NUM16(crcNum))
        print(msg)
        puerto.write(msg)

elif mode == 1:
    ID = 1006867427
    Address = 0x01
    Regs = [0xabcd, 0xf0f0]
    NRegs = len(Regs)
    coils = [0b0, 0b1]
    NCoils = len(coils)

    while 1:
        exCode = 0
        msg = []
        data = [puerto.read(1)]

        while puerto.inWaiting() > 0:
            data.append(puerto.read(1))
        dataN = Bar2Int(data)
        ad = dataN[0]
        fn = dataN[1]
        N0 = dataN[2] * 256 + dataN[3]
        N1 = dataN[4] * 256 + dataN[5]
        print(dataN)
        crcIn = dataN[len(dataN) - 2] * 256 + dataN[len(dataN) - 1]
        # print(crcIn)
        crcC = CRC_MOD16(dataN[0:len(dataN) - 2])
        # print(crcC)
        if ad == Address and crcIn == crcC:
            if fn == 1:  # Reald coils              adx8/fnx8/Nx8/coilsXNx8/crcx16
                if 1 <= N1 <= 2000:
                    if 0 <= N0 <= (NCoils - 1) and (N0 + N1) <= NCoils:
                        coilsOut = coils[N0:N1 + N0]
                        N = 0
                        if len(coilsOut) % 8 == 0:
                            N = len(coilsOut) / 8
                        else:
                            N = (len(coilsOut) // 8) + 1
                        msg.extend([Address, fn, N])
                        coilB = 0
                        ci = 0
                        for i in range(len(coilsOut)):
                            coilB += coilsOut[i] * pow(2, ci)
                            ci += 1
                            if ci == 8 or i == (len(coilsOut) - 1):
                                ci = 0
                                msg.append(coilB)
                                coilB = 0
                    else:
                        exCode = 2
                        msg.extend([Address, fn + 0x80, exCode])
                else:
                    exCode = 3
                    msg.extend([Address, fn + 0x80, exCode])

            elif fn == 3:  # Read holding registers
                if 1 <= N1 <= 125:
                    if 0 <= N0 <= (NRegs - 1) and (N0 + N1) <= NRegs:
                        regsOut = Regs[N0:N1 + N0]
                        N = len(regsOut) * 2
                        msg.extend([Address, fn, N])
                        for i in regsOut:
                            msg.extend(NUM16(i))
                    else:
                        exCode = 2
                        msg.extend([Address, fn + 0x80, exCode])
                else:
                    exCode = 3
                    msg.extend([Address, fn + 0x80, exCode])

            elif fn == 5:  # write single coil
                if N1 == 0x0000 or N1 == 0xFF00:
                    if 0 <= N0 <= (NCoils - 1):
                        if N1 == 0x0000:
                            coils[N0] = 0
                        elif N1 == 0xFF00:
                            coils[N0] = 1
                        msg.extend([Address, fn])
                        msg.extend(NUM16(N0))
                        msg.extend(NUM16(N1))
                    else:
                        exCode = 2
                        msg.extend([Address, fn + 0x80, exCode])
                else:
                    exCode = 3
                    msg.extend([Address, fn + 0x80, exCode])

            elif fn == 6:  # write single register
                if 0x0000 <= N1 <= 0xFFFF:
                    if 0 <= N0 <= (NRegs - 1):
                        Regs[N0] = N1
                        msg.extend([Address, fn])
                        msg.extend(NUM16(N0))
                        msg.extend(NUM16(N1))
                    else:
                        exCode = 2
                        msg.extend([Address, fn + 0x80, exCode])
                else:
                    exCode = 3
                    msg.extend([Address, fn + 0x80, exCode])

            elif fn == 15:  # write multiple coils
                N = dataN[6]
                if 1 <= N1 <= 0x7B0 and N == (len(dataN) - 9):
                    if 0 <= N0 <= (NCoils - 1) and (N0 + N1) <= NCoils:
                        ci = 0
                        for i in range(N1):
                            coils[N0 + i] = (dataN[7 + (i // 8)] % pow(2, ci + 1)) // pow(2, ci)
                            ci += 1
                            if ci == 8:
                                ci = 0
                        msg.extend([Address, fn])
                        msg.extend(NUM16(N0))
                        msg.extend(NUM16(N1))
                    else:
                        exCode = 2
                        msg.extend([Address, fn + 0x80, exCode])
                else:
                    exCode = 3
                    msg.extend([Address, fn + 0x80, exCode])

            elif fn == 16:  # write multiple registers
                N = dataN[6]
                if 1 <= N1 <= 0x7B and N == (len(dataN) - 9):
                    if 0 <= N0 <= (NRegs - 1) and (N0 + N1) <= NRegs:
                        for i in range(N1):
                            Regs[N0 + i] = dataN[7 + (2 * i)] * 256 + dataN[8 + (2 * i)]
                        msg.extend([Address, fn])
                        msg.extend(NUM16(N0))
                        msg.extend(NUM16(N1))
                    else:
                        exCode = 2
                        msg.extend([Address, fn + 0x80, exCode])
                else:
                    exCode = 3
                    msg.extend([Address, fn + 0x80, exCode])

            elif fn == 23:  # read/write multiple registers
                N2 = dataN[6] * 256 + dataN[7]
                N3 = dataN[8] * 256 + dataN[9]
                N = dataN[10]
                if 1 <= N1 <= 0x7D and 1 <= N3 <= 0x79 and N == (len(dataN) - 13):
                    if 0 <= N0 <= (NRegs - 1) and (N0 + N1) <= NRegs and 0 <= N2 <= (NRegs - 1) and (N2 + N3) <= NRegs:
                        for i in range(N3):
                            Regs[N2 + i] = dataN[11 + (2 * i)] * 256 + dataN[12 + (2 * i)]
                        regsOut = Regs[N0:N1 + N0]
                        N = len(regsOut) * 2
                        msg.extend([Address, fn, N])
                        for i in regsOut:
                            msg.extend(NUM16(i))
                    else:
                        exCode = 2
                        msg.extend([Address, fn + 0x80, exCode])
                else:
                    exCode = 3
                    msg.extend([Address, fn + 0x80, exCode])

            else:
                exCode = 1
                msg.extend([Address, fn + 0x80, exCode])

            crcNum = CRC_MOD16(msg)
            msg.extend(NUM16(crcNum))
            print(msg)
            puerto.write(msg)