# Multi-frame tkinter application v2.3
import tkinter as tk


class SampleApp(tk.Tk):
  def __init__(self, controller):
    tk.Tk.__init__(self)
    width = self.winfo_screenwidth()
    height = self.winfo_screenheight()
    self.geometry("%dx%d" % (width, height))
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self._frame = None
    self.switch_frame(StartPage, controller)

  def switch_frame(self, frame_class, controller):
    """Destroys current frame and replaces it with a new one."""
    new_frame = frame_class(self, controller)
    if self._frame is not None:
        self._frame.destroy()
    self._frame = new_frame
    self._frame.grid(row=0, column=0, sticky="nesw")


class StartPage(tk.Frame):
  def __init__(self, master, controller):
    self.controller = controller
    tk.Frame.__init__(self, master)
    tk.Label(self, text="Bienvenido a laplace").grid(
        row=0, column=0, columnspan=4)
    tk.Button(self, text="Enrolar",
              command=lambda: master.switch_frame(Enrolar, self.controller)).grid(row=1, column=0, sticky="nesw")
    tk.Button(self, text="Detectar",
              command=lambda: master.switch_frame(Detectar, self.controller)).grid(row=1, column=1, sticky="nesw")
    tk.Button(self, text="Eliminar",
              command=lambda: master.switch_frame(Eliminar, self.controller)).grid(row=1, column=2, sticky="nesw")
    tk.Button(self, text="Limpiar DB",
              command=lambda: master.switch_frame(Limpiar, self.controller)).grid(row=1, column=3, sticky="nesw")

    self.rowconfigure(0, weight=2)
    self.rowconfigure(1, weight=1)
    self.columnconfigure([0, 1, 2, 3], weight=1)


class Enrolar(tk.Frame):
  def __init__(self, master, controller):
    self.controller = controller
    self.master = master
    tk.Frame.__init__(self, master)
    tk.Label(self, text="Ingrese sus datos").grid(row=0, column=0, columnspan=4)
    tk.Label(self, text="Nombre").grid(row=1, column=0, columnspan=1)
    self.name_field = tk.Entry(self)
    self.name_field.grid(row=1, column=1, columnspan=2, sticky="ew")
    tk.Label(self, text="Telefono").grid(row=2, column=0, columnspan=1)
    self.phone_field = tk.Entry(self)
    self.phone_field.grid(row=2, column=1, columnspan=2, sticky="ew")
    tk.Button(self, text="Cancelar",
              command=lambda: self.master.switch_frame(StartPage, self.controller)).grid(row=3, column=0, columnspan=2,sticky="nesw")
    tk.Button(self, text="Continuar",
              command=lambda: self.verifyPersonData()).grid(row=3, column=2, columnspan=2, sticky="nesw")
    self.rowconfigure(0, weight=1)
    self.rowconfigure([1,2], weight=2)
    self.rowconfigure(3, weight=3)
    self.columnconfigure([0, 1, 2, 3], weight=1)
  
  def verifyPersonData(self):
    name = self.name_field.get()
    phone = self.phone_field.get()
    if self.controller.verifyPersonData(name, phone):
      self.master.switch_frame(StartPage, self.controller)

class Enrolando(tk.Frame):
  def __init__(self, master, controller):
    tk.Frame.__init__(self, master)

class Detectar(tk.Frame):
  def __init__(self, master, controller):
    tk.Frame.__init__(self, master)
    tk.Label(self, text="Detectando").grid(row=0, column=0, columnspan=2)
    tk.Button(self, text="Cancelar",
              command=lambda: master.switch_frame(StartPage)).grid(row=1, column=0, sticky="nesw")
    tk.Button(self, text="Continuar",
              command=lambda: master.switch_frame(StartPage)).grid(row=1, column=1, sticky="nesw")

    self.rowconfigure(0, weight=2)
    self.rowconfigure(1, weight=1)
    self.columnconfigure([0, 1], weight=1)


class Eliminar(tk.Frame):
  def __init__(self, master, controller):
    tk.Frame.__init__(self, master)
    tk.Label(self, text="Eliminando").grid(row=0, column=0, columnspan=2)
    tk.Button(self, text="Cancelar",
              command=lambda: master.switch_frame(StartPage)).grid(row=1, column=0, sticky="nesw")
    tk.Button(self, text="Continuar",
              command=lambda: master.switch_frame(StartPage)).grid(row=1, column=1, sticky="nesw")

    self.rowconfigure(0, weight=2)
    self.rowconfigure(1, weight=1)
    self.columnconfigure([0, 1], weight=1)


class Limpiar(tk.Frame):
  def __init__(self, master, controller):
    tk.Frame.__init__(self, master)
    tk.Label(self, text="Limpiando DB").grid(row=0, column=0, columnspan=2)
    tk.Button(self, text="Cancelar",
              command=lambda: master.switch_frame(StartPage)).grid(row=1, column=0, sticky="nesw")
    tk.Button(self, text="Continuar",
              command=lambda: master.switch_frame(StartPage)).grid(row=1, column=1, sticky="nesw")

    self.rowconfigure(0, weight=2)
    self.rowconfigure(1, weight=1)
    self.columnconfigure([0, 1], weight=1)
