import time
import tkinter as tk
from persona import Person
from tkinter import BooleanVar


class applicationController:
    def __init__(self, reader, repo) -> None:
        self.serialReader = reader
        self.repo = repo

    def enrollPerson(self, label: tk.Label, data: dict, enrolled: BooleanVar) -> bool:
        id = self.repo.get_all_count() + 1
        person = Person(data["name"], data["phone"])

        if self.serialReader.readUntilString("LISTO CARGA"):
            self.serialReader.writeInSerial("1")  # Modo enrolamiento en sensor
            if self.serialReader.readUntilString("NUMBER ID"):
                self.serialReader.writeInSerial(str(id))
                if self.serialReader.readUntilString("WAITING"):
                    label.configure(text="Coloque dedo en el sensor")
                    label.update()
                    if self.serialReader.readUntilString("Remove finger"):
                        label.configure(text="Retire dedo del sensor")
                        label.update()
                        time.sleep(3)
                        if self.serialReader.readUntilString("WAITING"):
                            label.configure(
                                text="Coloque dedo en el sensor nuevamente")
                            label.update()
                            if self.serialReader.readUntilString("Stored!"):
                                self.repo.add(person, id)
                                enrolled.set(True)
                                return
        enrolled.set(False)
        return

    def verifyPersonData(self, name: str, phone: str) -> bool:
        return name != "" and phone != ""
