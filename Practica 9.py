import threading
import time
import tkinter as tk

archivo_sem = threading.Semaphore(1)
archivo_contenido = ""
texto_editar = "Texto a editar en tiempo real."

def leer_archivo(ventana_id, text_widget):
    global archivo_contenido
    text_widget.delete('1.0', 'end')
    lectura_concurrente()
    for caracter in archivo_contenido:
        text_widget.insert('end', caracter)
        text_widget.update()
        time.sleep(0.1)  # Simula un pequeño retraso por carácter

def simular_escritura(ventana_id, text_widget):
    global archivo_contenido
    for caracter in texto_editar:
        archivo_sem.acquire()
        nuevo_contenido = archivo_contenido + caracter
        text_widget.delete('1.0', 'end')
        text_widget.insert('end', nuevo_contenido)
        text_widget.update()
        archivo_contenido = nuevo_contenido
        archivo_sem.release()
        time.sleep(0.1)  # Simula un pequeño retraso por carácter

def guardar_archivo(ventana_id, text_widget):
    global archivo_contenido
    archivo_sem.acquire()
    text_widget.delete('1.0', 'end')
    text_widget.insert('end', "Guardando...")
    text_widget.update()
    time.sleep(2)  # Simula un proceso de guardado de 2 segundos
    text_widget.delete('1.0', 'end')
    text_widget.insert('end', "Guardado completado.")
    text_widget.update()
    archivo_sem.release()

def lectura_concurrente():
    while archivo_sem._value == 0:  # Esperar a que se libere el archivo
        time.sleep(0.1)

def ventana(ventana_id):
    root = tk.Tk()
    root.title(f"Ventana {ventana_id}")
    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack()

    leer_button = tk.Button(root, text="Leer", command=lambda: leer_archivo(ventana_id, text_widget))
    editar_button = tk.Button(root, text="Editar")
    guardar_button = tk.Button(root, text="Guardar", command=lambda: guardar_archivo(ventana_id, text_widget))

    leer_button.pack()
    editar_button.pack()
    guardar_button.pack()

    # Agregar evento para iniciar la simulación de escritura
    editar_button.config(command=lambda: simular_escritura(ventana_id, text_widget))

    root.mainloop()

# Ejecutar las tres ventanas en hilos separados
thread1 = threading.Thread(target=ventana, args=(1,))
thread2 = threading.Thread(target=ventana, args=(2,))
thread3 = threading.Thread(target=ventana, args=(3,))

thread1.start()
thread2.start()
thread3.start()
