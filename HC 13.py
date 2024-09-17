import tkinter as tk
from tkinter import ttk, Toplevel
from collections import deque
import array  

historias = []  

cola_pacientes = deque()  

pila_historial = []  

ids_pacientes = array.array('i', [])  

def agregar_historia(historia):
    historias.append(historia)

def obtener_historia_paciente(paciente):
    for historia in historias:
        if historia.paciente == paciente:
            return historia
    return None

class HistoriaClinica:
    def __init__(self, paciente, fecha, diagnóstico, id):
        self.paciente = paciente
        self.fecha = fecha
        self.diagnostico = diagnóstico
        self.tratamiento = ""

class AplicacionHistoriasClinicas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Historias Clinicas")
        self.ventana.geometry("800x600")
        self.crear_interfaz()

    def crear_interfaz(self):
        self.frm_principal = ttk.Frame(self.ventana, padding="10")
        self.frm_principal.grid()

        self.btn_nuevo_paciente = ttk.Button(self.frm_principal, text="Nuevo Paciente", command=self.registrar_paciente)
        self.btn_nuevo_paciente.grid(row=0, column=0, pady=5)

        self.listbox_pacientes = tk.Listbox(self.frm_principal, selectmode=tk.SINGLE)
        self.listbox_pacientes.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W+tk.E)

        self.btn_abrir_carpeta = ttk.Button(self.frm_principal, text="Abrir Historia", command=self.abrir_carpeta)
        self.btn_abrir_carpeta.grid(row=2, column=0, pady=5)

    def registrar_paciente(self):
        ventana_registro = Toplevel(self.ventana)
        ventana_registro.title("Registro de Paciente")
        self.crear_interfaz_registro(ventana_registro)

    def crear_interfaz_registro(self, ventana):
        self.frm_registro = ttk.Frame(ventana, padding="10")
        self.frm_registro.pack()

        ttk.Label(self.frm_registro, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.txt_nombre = ttk.Entry(self.frm_registro, width=30)
        self.txt_nombre.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(self.frm_registro, text="Apellido:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.txt_apellido = ttk.Entry(self.frm_registro, width=30)
        self.txt_apellido.grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(self.frm_registro, text="Fecha:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.txt_fecha = ttk.Entry(self.frm_registro, width=30)
        self.txt_fecha.grid(row=2, column=1, sticky=tk.W, pady=5)

        nuevo_id = f"USR{len(historias) + 1:04d}"
        
        ttk.Label(self.frm_registro, text="ID:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.txt_id = ttk.Entry(self.frm_registro, width=30)
        self.txt_id.insert(0, nuevo_id)
        self.txt_id.config(state='readonly')
        self.txt_id.grid(row=3, column=1, sticky=tk.W, pady=5)

        self.btn_registrar = ttk.Button(self.frm_registro, text="Registrar", command=self.registrar_paciente_final)
        self.btn_registrar.grid(row=4, column=0, columnspan=2, pady=5)

    def registrar_paciente_final(self):
        nombre = self.txt_nombre.get()
        apellido = self.txt_apellido.get()
        fecha = self.txt_fecha.get()
        id = self.txt_id.get()

        paciente = f"{nombre} {apellido}"
        historia = HistoriaClinica(paciente, fecha, "", id)
        agregar_historia(historia)

        cola_pacientes.append(paciente)  

        ids_pacientes.append(len(historias) + 1) 

        self.listbox_pacientes.insert(tk.END, f"{nombre} {apellido} - {fecha} - ID: {id}")

        self.txt_nombre.delete(0, tk.END)
        self.txt_apellido.delete(0, tk.END)
        self.txt_fecha.delete(0, tk.END)

        ventana_registro = self.frm_registro.master
        ventana_registro.destroy()

    def abrir_carpeta(self):
        indice = self.listbox_pacientes.curselection()
        if indice:
            carpeta = self.listbox_pacientes.get(indice)
            paciente = carpeta.split("-")[0].strip()
            historia = obtener_historia_paciente(paciente)
            if historia:
                ventana_diagnostico = Toplevel(self.ventana)
                ventana_diagnostico.title(f"Diagnostico y Tratamiento - {paciente}")

                self.crear_interfaz_diagnostico(ventana_diagnostico, historia)
            else:
                ventana_diagnostico = Toplevel(self.ventana)
                ventana_diagnostico.title("Nuevo Diagnostico y Tratamiento")

                self.crear_interfaz_nuevo_diagnostico(ventana_diagnostico)

    def crear_interfaz_diagnostico(self, ventana, historia):
        self.frm_diagnostico = ttk.Frame(ventana, padding="10")
        self.frm_diagnostico.pack()

        ttk.Label(self.frm_diagnostico, text="Diagnostico:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.txt_diagnostico = ttk.Entry(self.frm_diagnostico, width=100)
        self.txt_diagnostico.insert(0, historia.diagnostico)
        self.txt_diagnostico.grid(row=1, column=0, sticky=tk.W, pady=5)

        ttk.Label(self.frm_diagnostico, text="Tratamiento:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.txt_tratamiento = ttk.Entry(self.frm_diagnostico, width=100)
        self.txt_tratamiento.insert(0, historia.tratamiento)
        self.txt_tratamiento.grid(row=3, column=0, sticky=tk.W, pady=5)

        self.btn_guardar = ttk.Button(self.frm_diagnostico, text="Actualizar", command=lambda: self.guardar_diagnostico_tratamiento(historia))
        self.btn_guardar.grid(row=4, column=0, pady=5)

    def guardar_diagnostico_tratamiento(self, historia):
        if historia:
            diagnostico = self.txt_diagnostico.get()
            tratamiento = self.txt_tratamiento.get()
            historia.diagnostico = diagnostico
            historia.tratamiento = tratamiento
            
            
            pila_historial.append(historia)  

            self.txt_diagnostico.delete(0, tk.END)
            self.txt_tratamiento.delete(0, tk.END)
        
        ventana_diagnostico = self.frm_diagnostico.master
        ventana_diagnostico.destroy()

    def crear_interfaz_nuevo_diagnostico(self, ventana):
        self.frm_nuevo_diagnostico = ttk.Frame(ventana, padding="10")
        self.frm_nuevo_diagnostico.pack()

        ttk.Label(self.frm_nuevo_diagnostico, text="Diagnostico:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.txt_nuevo_diagnostico = ttk.Entry(self.frm_nuevo_diagnostico, width=100)
        self.txt_nuevo_diagnostico.grid(row=1, column=0, sticky=tk.W, pady=5)

        ttk.Label(self.frm_nuevo_diagnostico, text="Tratamiento:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.txt_nuevo_tratamiento = ttk.Entry(self.frm_nuevo_diagnostico, width=100)
        self.txt_nuevo_tratamiento.grid(row=3, column=0, sticky=tk.W, pady=5)

        self.btn_guardar_nuevo = ttk.Button(self.frm_nuevo_diagnostico, text="Guardar", command=self.guardar_nuevo_diagnostico_tratamiento)
        self.btn_guardar_nuevo.grid(row=4, column=0, pady=5)

    def guardar_nuevo_diagnostico_tratamiento(self):
        nuevo_diagnostico = self.txt_nuevo_diagnostico.get()
        nuevo_tratamiento = self.txt_nuevo_tratamiento.get()
        paciente = self.txt_nuevo_diagnostico.master.title().split()[1]
        
        historia = HistoriaClinica(paciente, "", nuevo_diagnostico, len(historias) + 1)
        agregar_historia(historia)
        historia.tratamiento = nuevo_tratamiento
        
        pila_historial.append(historia)  

        self.txt_nuevo_diagnostico.delete(0, tk.END)
        self.txt_nuevo_tratamiento.delete(0, tk.END)
        ventana_nuevo_diagnostico = self.frm_nuevo_diagnostico.master
        ventana_nuevo_diagnostico.destroy()

def main():
    ventana = tk.Tk()
    aplicacion = AplicacionHistoriasClinicas(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()
