import time
import tkinter as tk
import json
from tkinter import ttk
from persona import Person
from tkinter import BooleanVar, Variable
from serial_service import SerialReader
from persona_repo import PersonRepository
from whatsapp_service import WhatsappService


class applicationController:
    def __init__(self, reader: SerialReader, repo: PersonRepository) -> None:
        self.serialReader = reader
        self.whatsappService = WhatsappService()
        self.repo = repo

    def enroll_person(self, label: tk.Label, data: dict, enrolled: BooleanVar) -> bool:
        id = self.repo.get_next_id()
        person = Person(data["name"], data["phone"])

        # TODO cambiar por excepciones
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
                            label.configure(text="Coloque dedo en el sensor nuevamente")
                            label.update()
                            if self.serialReader.readUntilString("Stored!"):
                                self.repo.add(person, id)
                                enrolled.set(True)
                                return
        enrolled.set(False)
        return

    def verifyPersonData(self, name: str, phone: str) -> bool:
        return name != "" and phone != ""

    def detect_finger(
        self, label: tk.Label, cancel_button: tk.Button, person: Variable, found: BooleanVar
    ) -> None:
        if self.serialReader.readUntilString("LISTO CARGA"):
            self.serialReader.writeInSerial("2")
            if self.serialReader.readUntilString("No finger detected"):
                label.configure(text="Coloque su dedo en el sensor")
                label.update()
                cancel_button.configure(state="normal")
                cancel_button.update()
                detected = self.serialReader.readUntilString(["Found ID #", "Did not find a match"] , timeout=0)
                if detected == "Found ID #":
                    self.cancel_deteccion()
                    line = self.serialReader.readNumberOfLines(1)
                    person_json = json.dumps(self.repo.get(int(line)).__dict__)
                    person.set(person_json)
                    found.set(True)
                    return
                elif detected == "Did not find a match":
                    found.set(False)
                    self.cancel_deteccion()
                    return
        self.cancel_deteccion()
        return

    def cancel_deteccion(self) -> None:
        self.serialReader.writeInSerial("999")

    def send_message(
        self, person: Person, sent: BooleanVar, entering: bool = True
    ) -> None:
        if entering:
            message: str = f"EL alumno {person.name} ha ingresado a Laplace"
        else:
            message: str = f"EL alumno {person.name} ha salido de Laplace"
        self.whatsappService.send_message(person.phone, message)
        sent.set(True)
        return
