import serial
import time
import estado


class SerialReader:
    def __init__(self) -> None:
        self.ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
        self.ser.reset_input_buffer()

    def reset(self) -> None:
        self.ser.close()
        self.ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
        self.ser.reset_input_buffer()

    def readFromSerial(self) -> str:
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode("utf-8").rstrip()
                return line

    def writeInSerial(self, text) -> None:
        self.ser.write(str(text).encode())

    # TODO log de lo conseguido desde el serial
    def readUntilString(self, strings, timeout=5):
        if isinstance(strings, str):
            strings = [strings]  # Convert a single string to a list with one element

        line = ""
        if timeout > 0:
            start_time = time.time()
            while time.time() - start_time < timeout:
                line = self.readFromSerial()
                print(line)
                if line in strings:
                    return True if len(strings) == 1 else line
            return False 
        else:
            while line not in strings:
                if estado.cancel_detect:
                    break
                line = self.readFromSerial()
                print(line)
            if line in strings:
                return True if len(strings) == 1 else line
            else:
                return False


    def readNumberOfLines(self, number) -> str:
        c = 0
        while c < number:
            line = self.readFromSerial()
            c += 1
        return line
