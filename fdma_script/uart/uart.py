import os
import sys
import serial
import serial.tools.list_ports

class uart_list():
    def __init__(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) == 0:
            print("No serial port available!!!")
        else:
            for i in port_list:
                print(i)

class uart():
    def __init__(self, port, bps):
        self.portx = port
        self.bps = bps
        self.serial = None

    def open(self):
        try:
            self.serial = serial.Serial(self.portx, self.bps, timeout = 0.1)
        except Exception as e:
            print(e)
            print("Can't open %s" % self.portx.upper())
            exit(-1)

    def close(self):
        self.serial.close()
        self.serial = None

    def reset(self):
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def read(self, num, timeout = 0.1):
        if timeout:
            self.serial.timeout = timeout

        return self.serial.read(num)

    def read_all(self):
        return self.serial.read_all()

    def readline(self):
        return self.serial.readline()

    def readlines(self):
        return self.serial.readlines()

    def write(self, s, timeout = 0.1):
        if timeout:
            self.serial.timeout = timeout

        return self.serial.write(s.encode('utf-8'))



