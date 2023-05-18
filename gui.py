# Multi-frame tkinter application v2.3
import json
import threading
import time
import tkinter as tk
from tkinter import BooleanVar, Variable, ttk
import estado
from applicationController import applicationController
from persona import Person


class App(tk.Tk):
    def __init__(self, controller: applicationController):
        tk.Tk.__init__(self)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._frame = None
        self.switch_frame(StartPage, controller)

    def switch_frame(self, frame_class: tk.Frame, controller: applicationController, data={}):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, controller, data)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0, sticky="nesw")
        self._frame.process()


class StartPage(tk.Frame):
    def __init__(self, master, controller: applicationController, data):
        self.controller = controller
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Bienvenido a laplace").grid(
            row=0, column=0, columnspan=4)
        tk.Button(self, text="Enrolar",
                  command=lambda: master.switch_frame(Enroll, self.controller)).grid(row=1, column=0, sticky="nesw")
        tk.Button(self, text="Detectar",
                  command=lambda: master.switch_frame(Detect, self.controller)).grid(row=1, column=1, sticky="nesw")
        tk.Button(self, text="Eliminar",
                  command=lambda: master.switch_frame(Delete, self.controller)).grid(row=1, column=2, sticky="nesw")
        tk.Button(self, text="Limpiar DB",
                  command=lambda: master.switch_frame(Clear, self.controller)).grid(row=1, column=3, sticky="nesw")

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure([0, 1, 2, 3], weight=1)

    def process(self):
        pass


class Enroll(tk.Frame):
    def __init__(self, master, controller, data):
        # Definimos items de pagina
        self.controller = controller
        self.master = master
        tk.Frame.__init__(self, master)
        form_title = tk.Label(self, text="Ingrese sus datos")
        name_label = tk.Label(self, text="Nombre")
        self.name_field = tk.Entry(self)
        phone_label = tk.Label(self, text="Telefono")
        self.phone_field = tk.Entry(self)
        cancel_button = tk.Button(self, text="Cancelar",
                                  command=lambda: self.master.switch_frame(StartPage, self.controller))
        continue_button = tk.Button(self, text="Continuar",
                                    command=lambda: self.verifyPersonData())

        # Definimos posiciones de elementos
        form_title.grid(row=0, column=0, columnspan=4)
        name_label.grid(row=1, column=0, columnspan=1)
        self.name_field.grid(row=1, column=1, columnspan=2, sticky="ew")
        phone_label.grid(row=2, column=0, columnspan=1)
        self.phone_field.grid(row=2, column=1, columnspan=2, sticky="ew")
        cancel_button.grid(row=3, column=0, columnspan=2, sticky="nesw")
        continue_button.grid(row=3, column=2, columnspan=2, sticky="nesw")

        # Definimos layout de la pagina
        self.rowconfigure(0, weight=1)
        self.rowconfigure([1, 2], weight=2)
        self.rowconfigure(3, weight=3)
        self.columnconfigure([0, 1, 2, 3], weight=1)

    def verifyPersonData(self):
        """ Envia datos a controller para validacion de datos de persona """
        name = self.name_field.get()
        phone = self.phone_field.get()
        if self.controller.verifyPersonData(name, phone):
            self.master.switch_frame(Enrolling, self.controller, data={
                                     "name": name, "phone": phone})

    def process(self):
        pass


class Enrolling(tk.Frame):
    def __init__(self, master, controller: applicationController, data):
        self.controller = controller
        self.master = master
        self.data = data
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text="Comenzando enrolamiento")
        cancel_button = tk.Button(
            self, text="Cancelar", command=lambda: master.switch_frame(StartPage, controller))

        self.label.grid(row=0, column=0)
        cancel_button.grid(row=1, column=0, sticky="nesw")

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def process(self):
        self.after(1000, lambda: self.start_enroll(self.master, self.data))

    def start_enroll(self, master, data):
        self.enrolled = BooleanVar()
        self.enrolled.set(False)
        self.enrolled.trace_add("write", self.check_complete)
        thread = threading.Thread(
            target=lambda: self.controller.enroll_person(self.label, self.data, self.enrolled))
        thread.start()

    def check_complete(self, *args):
        # TODO
        if self.enrolled.get():
            self.label.configure(text="Enrolado!")
            self.label.update
        else:
            self.label.configure(text="se callo la wea :c")
            self.label.update


class Detect(tk.Frame):
    def __init__(self, master, controller: applicationController, data):
        self.controller = controller
        self.master = master
        tk.Frame.__init__(self, master)
        # TODO Agrandar font de texto
        self.label = tk.Label(self, text="Iniciando detección")
        # TODO Funcionalidad cancelar
        self.cancel_button = tk.Button(self, text="Cancelar", command=self.cancel_deteccion, state="disabled")

        self.label.grid(row=0, column=0, columnspan=2)
        self.cancel_button.grid(row=1, column=0, sticky="nesw")

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def process(self):
        self.after(100, lambda: self.start_deteccion(self.label))

    def cancel_deteccion(self):
        estado.cancel_detect = True
        self.thread.join()
        estado.cancel_detect = False
        self.master.switch_frame(StartPage, self.controller)

    def start_deteccion(self, label: tk.Label) -> None:
        self.person = Variable()
        self.person.set(None)
        self.person.trace_add("write", self.check_person)
        self.thread = threading.Thread(
            target=lambda: self.controller.detect_finger(self.label, self.cancel_button, self.person))
        self.thread.start()

    def check_person(self, *args):
        # TODO caerse (comenzar de nuevo) cuando persona no es encontrada?
        # try:
        person_instance = Person(**json.loads(self.person.get()))
        self.master.switch_frame(
            Detected, self.controller, data=person_instance)
        # except:
        #     self.label.configure(
        #         text="Hubo un error, empezando la deteccion nuevamente")
        #     self.after(1000, lambda: self.start_deteccion(self.label))


class Detected(tk.Frame):
    def __init__(self, master, controller: applicationController, data: Person):
        self.controller = controller
        self.person = data
        self.master = master
        tk.Frame.__init__(self, master)
        title = tk.Label(self, text="Se detecto a la siguiente persona")
        person_data = tk.Label(self, text="Nombre: " +
                               self.person.name + " Telefono: " + self.person.phone)
        self.sending_label = tk.Label(self)
        cancel_button = tk.Button(
            self, text="Cancelar", command=lambda: master.switch_frame(Detect, self.controller))
        confirm_button = tk.Button(self, text="Continuar", command= self.send_message )

        title.grid(row=0, column=0, columnspan=2)
        person_data.grid(row=1, column=0, columnspan=2)
        self.sending_label.grid(row=2, column=0, columnspan=2)
        cancel_button.grid(row=3, column=0, sticky="nesw")
        confirm_button.grid(row=3, column=1, sticky="nesw")

        self.rowconfigure([0, 1, 2], weight=2)
        self.rowconfigure(3, weight=3)
        self.columnconfigure([0,1], weight=1)

    def send_message(self):
        self.sending_label.configure(text="Enviando mensaje")
        self.sending_label.update()
        self.sent = BooleanVar()
        self.sent.set(False)
        self.sent.trace_add("write", self.check_sent)
        thread = threading.Thread(
            target=lambda: self.controller.send_message(self.person, self.sent))
        thread.start()

    def check_sent(self, *args):
        if self.sent.get():
            self.sending_label.configure(text="Mensaje enviado!")
            self.after(1000, lambda: self.master.switch_frame(Detect, self.controller))

    def process(self):
        pass


class Delete(tk.Frame):
    def __init__(self, master, controller, data):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Eliminando").grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Cancelar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=0, sticky="nesw")
        tk.Button(self, text="Continuar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=1, sticky="nesw")

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure([0, 1], weight=1)

    def process(self):
        pass


class Clear(tk.Frame):
    def __init__(self, master, controller, data):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Limpiando DB").grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Cancelar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=0, sticky="nesw")
        tk.Button(self, text="Continuar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=1, sticky="nesw")

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure([0, 1], weight=1)

    def process(self):
        pass
