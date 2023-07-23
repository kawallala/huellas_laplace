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
        self.resizable(False, True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._frame = None
        self.switch_frame(StartPage, controller)

    def switch_frame(
        self, frame_class: tk.Frame, controller: applicationController, data={}
    ):
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
        tk.Label(self, text="Bienvenido a laplace").grid(row=0, column=0, columnspan=4)
        tk.Button(
            self,
            text="Enrolar",
            command=lambda: master.switch_frame(Enroll, self.controller),
        ).grid(row=1, column=0, sticky="nesw")
        tk.Button(
            self,
            text="Detectar",
            command=lambda: master.switch_frame(Detect, self.controller),
        ).grid(row=1, column=1, sticky="nesw")
        tk.Button(
            self,
            text="Eliminar",
            command=lambda: master.switch_frame(Delete, self.controller),
        ).grid(row=1, column=2, sticky="nesw")

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure([0, 1, 2], weight=1)

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
        cancel_button = tk.Button(
            self,
            text="Cancelar",
            command=lambda: self.master.switch_frame(StartPage, self.controller),
        )
        continue_button = tk.Button(
            self, text="Continuar", command=lambda: self.verifyPersonData()
        )

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
        """Envia datos a controller para validacion de datos de persona"""
        name = self.name_field.get()
        phone = self.phone_field.get()
        if self.controller.verifyPersonData(name, phone):
            self.master.switch_frame(
                Enrolling, self.controller, data={"name": name, "phone": phone}
            )

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
            self,
            text="Cancelar",
            command=lambda: master.switch_frame(StartPage, controller),
        )

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
            target=lambda: self.controller.enroll_person(
                self.label, self.data, self.enrolled
            )
        )
        thread.start()

    def check_complete(self, *args):
        # TODO
        if self.enrolled.get():
            self.label.configure(text="Enrolado!")
            self.label.update
            self.after(1000, self.master.switch_frame, StartPage, self.controller)
        else:
            self.label.configure(text="Ha ocurrido un error")
            self.label.update


# TODO Asegurarse de que al menos hay una persona en la DB
class Detect(tk.Frame):
    def __init__(self, master, controller: applicationController, data=None):
        self.controller = controller
        self.master = master
        tk.Frame.__init__(self, master)
        # TODO Agrandar font de texto
        self.label = tk.Label(self, text="Iniciando detección")
        # TODO Funcionalidad cancelar
        self.cancel_button = tk.Button(
            self, text="Cancelar", command=self.cancel_deteccion, state="disabled"
        )

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
        self.found = BooleanVar()
        self.found.set(False)
        self.person = Variable()
        self.person.set(None)
        self.found.trace_add("write", self.check_person)
        self.thread = threading.Thread(
            target=lambda: self.controller.detect_finger(
                self.label, self.cancel_button, self.person, self.found
            )
        )
        self.thread.start()

    def check_person(self, *args):
        if self.found.get():
            person_instance = Person(**json.loads(self.person.get()))
            self.master.switch_frame(Detected, self.controller, data=person_instance)
        else:
            self.cancel_button.configure(state="disabled")
            self.label.configure(
                text="No se encontro a la persona, empezando la deteccion nuevamente"
            )
            self.after(500, lambda: self.start_deteccion(self.label))


class Detected(tk.Frame):
    def __init__(self, master, controller: applicationController, data: Person):
        self.controller = controller
        self.person = data
        self.master = master
        tk.Frame.__init__(self, master)
        title = tk.Label(self, text="Se detecto a la siguiente persona")
        person_data = tk.Label(
            self, text="Nombre: " + self.person.name + " Telefono: " + self.person.phone
        )
        self.sending_label = tk.Label(self)
        cancel_button = tk.Button(
            self,
            text="Cancelar",
            command=lambda: master.switch_frame(Detect, self.controller),
        )
        confirm_button_entrance = tk.Button(
            self, text="Entrando", command=lambda: self.send_message()
        )
        confirm_button_exit = tk.Button(
            self, text="Saliendo", command=lambda: self.send_message(entrance=False)
        )

        title.grid(row=0, column=0, columnspan=3)
        person_data.grid(row=1, column=0, columnspan=3)
        self.sending_label.grid(row=2, column=0, columnspan=3)
        cancel_button.grid(row=3, column=0, sticky="nesw")
        confirm_button_entrance.grid(row=3, column=1, sticky="nesw")
        confirm_button_exit.grid(row=3, column=2, sticky="nesw")

        self.rowconfigure([0, 1, 2], weight=2)
        self.rowconfigure(3, weight=3)
        self.columnconfigure([0, 1, 2], weight=1)

    def send_message(self, entrance=True):
        self.sending_label.configure(text="Enviando mensaje")
        self.sending_label.update()
        self.sent = BooleanVar()
        self.sent.set(False)
        self.sent.trace_add("write", self.check_sent)
        thread = threading.Thread(
            target=lambda: self.controller.send_message(
                self.person, self.sent, entering=entrance
            )
        )
        thread.start()

    def check_sent(self, *args):
        if self.sent.get():
            self.sending_label.configure(text="Mensaje enviado!")
            self.after(2000, self.master.switch_frame, Detect, self.controller)
        else:
            self.sending_label.configure(text="Ocurrio un error")

    def return_detect(self):
        self.master.switch_frame(Detect, self.controller)

    def process(self):
        pass


class Delete(tk.Frame):
    def __init__(self, master: App, controller: applicationController, data):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.master = master
        self.tree = ttk.Treeview(self, column=("c1", "c2"), show="headings")
        self.tree.heading("#0", text="ID")
        self.tree.column("#0", minwidth=50, width=50, anchor="center")
        self.tree.heading("c1", text="Nombre")
        self.tree.column("c1", minwidth=100, width=100, anchor="center")
        self.tree.heading("c2", text="Telefono")
        self.tree.column("c2", minwidth=100, width=100, anchor="center")
        data = controller.get_all_person_data()
        for row in data:
            self.tree.insert(
                "", "end", text=row.doc_id, values=(row["name"], row["phone"])
            )
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        cancel_button = tk.Button(
            self,
            text="Cancelar",
            command=lambda: master.switch_frame(StartPage, controller),
        )
        self.tree.grid(row=0, column=1, columnspan=8, sticky="nesw")
        self.vsb.grid(row=0, column=9, sticky="nsw")
        cancel_button.grid(row=1, column=0, columnspan=10, sticky="nesw")

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure([i for i in range(10)], weight=1)

    def process(self):
        self.tree.bind("<<TreeviewSelect>>", self.row_selected)
        self.tree.configure(yscrollcommand=self.vsb.set)

    def row_selected(self, event):
        selected_item = self.tree.focus()  # Get the selected item (row)
        item_data = self.tree.item(selected_item)
        print(item_data)
        row_values = item_data["values"]

        # Perform desired actions with the row values
        print("Selected Row:", row_values)
        # Add your custom code here
        person = self.controller.get_person_data(item_data["text"])
        self.master.switch_frame(ForDeletion, self.controller, int(item_data["text"]))


class ForDeletion(tk.Frame):
    def __init__(self, master, controller: applicationController, data: int):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.person = self.controller.get_person_data(data)
        title = tk.Label(
            self,
            text="Seguro que quiere eliminar a:\n\n\nNombre: "
            + self.person.name
            + " Telefono: "
            + self.person.phone,
        )
        cancel_button = tk.Button(
            self,
            text="Cancelar",
            command=lambda: master.switch_frame(StartPage, self.controller),
        )
        delete_button = tk.Button(
            self,
            text="Eliminar",
            command=lambda: self.delete_person(data),
        )

        title.grid(row=0, column=0, columnspan=2)
        cancel_button.grid(row=1, column=0, sticky="nesw")
        delete_button.grid(row=1, column=1, sticky="nesw")

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure([0, 1], weight=1)

    def process(self):
        pass

    def delete_person(self, id: int):
        self.deleted = BooleanVar()
        self.deleted.set(False)
        self.deleted.trace_add("write", self.check_deleted)
        thread = threading.Thread(
            target=lambda: self.controller.delete_person(id, self.deleted)
        )
        thread.start()

    def check_deleted(self, *args):
        self.master.switch_frame(Delete, self.controller)
