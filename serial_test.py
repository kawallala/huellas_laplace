import serial


class SerialReader():
    def __init__(self) -> None:
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def readFromSerial(self):
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').rstrip()
                return line

    def writeInSerial(self, text):
        self.ser.write(str(text).encode())

    def readUntilString(self, string):
        line = ""
        while (string != line):
            line = self.readFromSerial()
            print(line)
        return True

    def readNumberOfLines(self, number):
        c = 0
        while (c < 0):
            line = self.readFromSerial()
            c += 1
        return line


if __name__ == '__main__':
    serialreader = SerialReader()
    serialreader.readUntilString("LISTO CARGA")
    serialreader.writeInSerial("1")
    serialreader.readUntilString("NUMBER ID")
