import serial
import time
import estado

class SerialReader:
    def __init__(self, app_logger) -> None:
        self.ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
        self.ser.reset_input_buffer()
        self.app_logger = app_logger

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
        self.app_logger.debug(f"Escribiendo en el puerto serial: {text}")
        self.ser.write(str(text).encode())

    # TODO log de lo conseguido desde el serial
    def readUntilString(self, strings, timeout=10):
        self.app_logger.debug(f"Detectando las cadenas: {strings}")
        if isinstance(strings, str):
            strings = [
                strings
            ]  # Convertir una cadena individual en una lista con un elemento

        line = ""
        if timeout > 0:
            start_time = time.time()
            while time.time() - start_time < timeout:
                line = self.readFromSerial()
                self.app_logger.debug(f"Línea leída desde el serial: {line}")
                if line in strings:
                    return True if len(strings) == 1 else line
            self.app_logger.warning(
                "Tiempo de espera agotado, no se encontró ninguna de las cadenas especificadas."
            )
            return False
        else:
            while line not in strings:
                if estado.cancel_detect:
                    self.app_logger.warning("Cancelado por usuario")
                    self.writeInSerial("999")
                    break
                line = self.readFromSerial()
                self.app_logger.debug(f"Línea leída desde el serial: {line}")

            if line in strings:
                return True if len(strings) == 1 else line
            else:
                self.app_logger.warning("No se encontró ninguna de las cadenas especificadas.")
                return False

    def readNumberOfLines(self, number) -> str:
        c = 0
        while c < number:
            line = self.readFromSerial()
            c += 1
        return line
