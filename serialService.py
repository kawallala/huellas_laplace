import serial
import time

class SerialReader():
  def __init__(self) -> None:
    self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    self.ser.reset_input_buffer()

  def readFromSerial(self) -> str:
    while True:
      if self.ser.in_waiting > 0:
        line = self.ser.readline().decode('utf-8').rstrip()
        return line

  def writeInSerial(self, text) -> None:
    self.ser.write(str(text).encode())

  def readUntilString(self, string, timeout = 10) -> bool:
    line = ""
    start_time = time.time()
    while time.time() - start_time < timeout:
      while (string != line):
              line = self.readFromSerial()
              print(line)
      return True
    return False

  def readNumberOfLines(self, number) -> str:
    c = 0
    while (c < number):
            line = self.readFromSerial()
            c += 1
    return line
  
  def enrollFinger(self, id) -> bool:
    if self.readUntilString("LISTO CARGA"):
      self.writeInSerial("1")
      if self.readUntilString("NUMBER ID"):
        self.writeInSerial(str(id))
        if self.readUntilString("Stored!"):
           return True
    return False