# Multi-frame tkinter application v2.3
import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        width= self.winfo_screenwidth()               
        height= self.winfo_screenheight()               
        self.geometry("%dx%d" % (width, height))
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0, sticky="nesw")

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Bienvenido a laplace").grid(row=0, column=0, columnspan=4)
        tk.Button(self, text="Enrolar",
                  command=lambda: master.switch_frame(Enrolar)).grid(row=1, column=0, sticky="nesw")
        tk.Button(self, text="Detectar",
                  command=lambda: master.switch_frame(Detectar)).grid(row=1, column=1, sticky="nesw")
        tk.Button(self, text="Eliminar",
                  command=lambda: master.switch_frame(Eliminar)).grid(row=1, column=2, sticky="nesw")
        tk.Button(self, text="Limpiar DB",
                  command=lambda: master.switch_frame(Limpiar)).grid(row=1, column=3, sticky="nesw")
        
        self.rowconfigure([0,1], weight=1)
        self.columnconfigure([0,1,2,3], weight=1)

class Enrolar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Enrolando").grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Cancelar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=0, sticky="nesw")
        tk.Button(self, text="Continuar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=1, sticky="nesw")
        
        self.rowconfigure([0,1], weight=1)
        self.columnconfigure([0,1], weight=1)

class Detectar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Detectando").grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Cancelar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=0, sticky="nesw")
        tk.Button(self, text="Continuar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=1, sticky="nesw")
        
        self.rowconfigure([0,1], weight=1)
        self.columnconfigure([0,1], weight=1)

class Eliminar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Eliminando").grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Cancelar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=0, sticky="nesw")
        tk.Button(self, text="Continuar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=1, sticky="nesw")
        
        self.rowconfigure([0,1], weight=1)
        self.columnconfigure([0,1], weight=1)

class Limpiar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Limpiando DB").grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Cancelar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=0, sticky="nesw")
        tk.Button(self, text="Continuar",
                  command=lambda: master.switch_frame(StartPage)).grid(row=1, column=1, sticky="nesw")
        
        self.rowconfigure([0,1], weight=1)
        self.columnconfigure([0,1], weight=1)