import serial
import time
import estado

class SerialReader():
    def __init__(self) -> None:
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def reset(self) -> None:
        self.ser.close()
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def readFromSerial(self) -> str:
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').rstrip()
                return line

    def writeInSerial(self, text) -> None:
        self.ser.write(str(text).encode())

    # TODO log de lo conseguido desde el serial
    def readUntilString(self, string, timeout=10) -> bool:
        line = ""
        if timeout > 0:
            start_time = time.time()
            while time.time() - start_time < timeout:
                line = self.readFromSerial()
                print(line)
                if (line == string):
                    return True
            return False
        else:
            while line != string:
                if estado.cancel_detect == True:
                    break
                line = self.readFromSerial()
                print(line)
            return line == string

    def readNumberOfLines(self, number) -> str:
        c = 0
        while (c < number):
            line = self.readFromSerial()
            c += 1
        return line
