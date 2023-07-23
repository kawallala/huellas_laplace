import time
import tkinter as tk
import json
from tkinter import ttk
from persona import Person
from tkinter import BooleanVar, Variable
from serial_service import SerialReader
from persona_repo import PersonRepository
from whatsapp_service import WhatsappService
import os
import logging
import logging.handlers


class applicationController:
    def __init__(self, reader: SerialReader, repo: PersonRepository) -> None:
        logging.basicConfig(
            filename="myapp.log",
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s:%(message)s",
        )
        self.serialReader = reader
        self.whatsappService = WhatsappService()
        self.repo = repo

    def enroll_person(self, label: tk.Label, data: dict, enrolled: BooleanVar) -> bool:
        logging.info(f"Enrolando a persona {str(data)}")
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
                                    logging.info(f"Persona Enrolada")
                                    self.repo.add(person, id)
                                    enrolled.set(True)
                                    return
            enrolled.set(False)
            return
        except Exception as e:
            logging.error("Ha ocurrido un error", exc_info=True)

    def delete_person(self, id: int, deleted: BooleanVar):
        logging.info(f"Intentando eliminar persona con ID: {id}")
        self.serialReader.writeInSerial("999")
        if self.serialReader.readUntilString("LISTO CARGA"):
            logging.debug("Recibida respuesta 'LISTO CARGA' del lector serial.")
            self.serialReader.writeInSerial("3")  # Modo borrado

            if self.serialReader.readUntilString("ID"):
                logging.debug("Recibida solicitud de 'ID' del lector serial.")
                self.serialReader.writeInSerial(str(id))

                if self.serialReader.readUntilString("Deleted!"):
                    logging.debug(f"Persona con ID {id} eliminada exitosamente.")
                    self.repo.delete(id)
                    deleted.set(True)
                    logging.info(f"Persona con ID {id} eliminada del repositorio.")
                    return

        logging.warning(f"No se pudo eliminar persona con ID {id}")
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
        logging.info("Iniciando detección de huella...")
        self.serialReader.writeInSerial("999")
        logging.debug("Escrito 999 en el lector serial.")
        detected =  self.serialReader.readUntilString(["LISTO CARGA", "No finger detected"])
        if detected == "LISTO CARGA":
            self.serialReader.writeInSerial("2")  # Modo deteccion en sensor
            self.serialReader.readUntilString("No finger detected")
        logging.debug("No se detectó ningún dedo en el sensor.")
        label.configure(text="Coloque su dedo en el sensor")
        label.update()
        cancel_button.configure(state="normal")
        cancel_button.update()

        detected = self.serialReader.readUntilString(
            ["Found ID #", "Did not find a match"], timeout=0
        )

        if detected == "Found ID #":
            logging.debug("Huella detectada y coincidencia encontrada.")
            self.cancel_deteccion()
            line = self.serialReader.readNumberOfLines(1)
            person_json = json.dumps(self.repo.get(int(line)).__dict__)
            person.set(person_json)
            found.set(True)
            logging.info("Huella detectada y coincidencia encontrada.")
            return
        elif detected == "Did not find a match":
            logging.debug("Huella detectada, pero no se encontró coincidencia.")
            self.cancel_deteccion()
            found.set(False)
            return

        logging.warning("No se pudo realizar la detección de huella.")
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
