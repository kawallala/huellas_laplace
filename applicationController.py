import time
import tkinter as tk
import json
from tkinter import ttk
from persona import Person
from tkinter import BooleanVar, Variable
from serial_service import SerialReader
from persona_repo import PersonRepository
from whatsapp_service import WhatsappService
import logging
import logging.handlers


class applicationController:
    def __init__(self, reader: SerialReader, repo: PersonRepository, app_logger, person_logger) -> None:
        self.serialReader = reader
        self.whatsappService = WhatsappService()
        self.repo = repo
        self.app_logger = app_logger
        self.person_logger = person_logger

    def enroll_person(self, label: tk.Label, data: dict, enrolled: BooleanVar) -> bool:
        self.app_logger.info(f"Enrolando a persona {str(data)}")
        id = self.repo.get_next_id()
        person = Person(data["name"], data["phone"])

        # TODO cambiar por excepciones
        try:
            self.serialReader.writeInSerial("999")
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
                                    text="Coloque dedo en el sensor nuevamente"
                                )
                                label.update()
                                if self.serialReader.readUntilString("Stored!"):
                                    self.app_logger.info(f"Persona Enrolada")
                                    self.repo.add(person, id)
                                    enrolled.set(True)
                                    return
            enrolled.set(False)
            return
        except Exception as e:
            self.app_logger.error("Ha ocurrido un error", exc_info=True)

    def delete_person(self, id: int, deleted: BooleanVar):
        self.app_logger.info(f"Intentando eliminar persona con ID: {id}")
        self.serialReader.writeInSerial("999")
        if self.serialReader.readUntilString("LISTO CARGA"):
            self.app_logger.debug("Recibida respuesta 'LISTO CARGA' del lector serial.")
            self.serialReader.writeInSerial("3")  # Modo borrado

            if self.serialReader.readUntilString("ID"):
                self.app_logger.debug("Recibida solicitud de 'ID' del lector serial.")
                self.serialReader.writeInSerial(str(id))

                if self.serialReader.readUntilString("Deleted!"):
                    self.app_logger.debug(f"Persona con ID {id} eliminada exitosamente.")
                    self.repo.delete(id)
                    deleted.set(True)
                    self.app_logger.info(f"Persona con ID {id} eliminada del repositorio.")
                    return

        self.app_logger.warning(f"No se pudo eliminar persona con ID {id}")
        deleted.set(False)
        return

    def verifyPersonData(self, name: str, phone: str) -> bool:
        return name != "" and phone != ""

    def get_person_data(self, id: int):
        return self.repo.get(id)

    def get_all_person_data(self):
        return self.repo.get_all()

    def detect_finger(
        self,
        label: tk.Label,
        cancel_button: tk.Button,
        person: Variable,
        found: BooleanVar,
    ) -> None:
        self.app_logger.info("Iniciando detección de huella...")
        if self.serialReader.readUntilString("LISTO CARGA"):
            self.app_logger.debug("Sensor preparando, iniciando modo deteccion")
            self.serialReader.writeInSerial("2")  # Modo deteccion en sensor
            if self.serialReader.readUntilString("No finger detected"):
                self.app_logger.debug("Sensor en modo deteccion")
                label.configure(text="Coloque su dedo en el sensor")
                label.update()
                cancel_button.configure(state="normal")
                cancel_button.update()
                detected = self.serialReader.readUntilString(
                    ["Found ID #", "Did not find a match"], timeout=0
                )

                if detected == "Found ID #":
                    self.app_logger.debug("Huella detectada y coincidencia encontrada.")
                    line = self.serialReader.readNumberOfLines(1)
                    person_json = json.dumps(self.repo.get(int(line)).__dict__)
                    person.set(person_json)
                    found.set(True)
                    return
                elif detected == "Did not find a match":
                    self.app_logger.debug("Huella detectada, pero no se encontró coincidencia.")
                    found.set(False)
                    return
            else:
                self.app_logger.warning("Ha ocurrido un error al iniciar la deteccion.")
                label.configure(text="Ha ocurrido un error al iniciar el sensor")
                label.update()
                found.set(False)
                return

        self.app_logger.warning("No se pudo realizar la detección de huella.")
        return

    def send_message(self, person: Person, sent: BooleanVar, entering: bool = True) -> None:
        if entering:
            message: str = f"EL alumno {person.name} ha ingresado a Laplace"
            self.person_logger.info(f"El alumno {person.name} ha ingresado a Laplace, numero: {person.phone}")
        else:
            message: str = f"EL alumno {person.name} ha salido de Laplace"
            self.person_logger.info(f"El alumno {person.name} ha salido a Laplace, numero: {person.phone}")

        self.whatsappService.send_message(person.phone, message)

        self.app_logger.info(f"Mensaje enviado a {person.name} ({person.phone}): {message}")
        # Log the message sending

        sent.set(True)
        return
