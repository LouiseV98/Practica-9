import threading
import time
import tkinter as tk

archivo_Semaforo = threading.Semaphore(1)
edicion_Semaforo = threading.Semaphore(1)
contenido_Archivo = ""
texto_Editar = "Lorem ipsum dolor sit amet, consectetur adipisicing elitin, sed do eiusmod tempor tur adipisicing elitin, sed do eiusmod tempor tur adipisicing elitin, sed do eiusmod tempor"

ventanas_Editando = []
ventanas_Leyendo = 0

def leer_archivo(ventana_Id, texto_Ventana):
    global contenido_Archivo, ventanas_Leyendo
    archivo_Semaforo.acquire()
    ventanas_Leyendo += 1
    if ventanas_Leyendo == 1:
        edicion_Semaforo.acquire()  # Bloquear edición si es la primera ventana en leer
    archivo_Semaforo.release()
    texto_Ventana.delete('1.0', 'end')
    lectura_concurrente()
    for caracter in contenido_Archivo:
        texto_Ventana.insert('end', caracter)
        texto_Ventana.update()
        time.sleep(0.1)
    archivo_Semaforo.acquire()
    ventanas_Leyendo -= 1
    if ventanas_Leyendo == 0:
        edicion_Semaforo.release()  # Desbloquear edición si no hay ventanas leyendo
    archivo_Semaforo.release()

def simular_escritura(ventana_Id, texto_Ventana):
    global contenido_Archivo
    archivo_Semaforo.acquire()
    edicion_Semaforo.acquire()
    ventanas_Editando.append(ventana_Id)  # Agregar ventana a la lista de edición
    for caracter in texto_Editar:
        nuevo_Contenido = contenido_Archivo + caracter
        texto_Ventana.delete('1.0', 'end')
        texto_Ventana.insert('end', nuevo_Contenido)
        texto_Ventana.update()
        contenido_Archivo = nuevo_Contenido
        time.sleep(0.1)
    ventanas_Editando.remove(ventana_Id)  # Eliminar ventana de la lista de edición
    edicion_Semaforo.release()
    archivo_Semaforo.release()

def guardar_archivo(ventana_Id, texto_Ventana):
    global contenido_Archivo
    archivo_Semaforo.acquire()
    edicion_Semaforo.acquire()
    while len(ventanas_Editando) > 0 or ventanas_Leyendo > 0:  # Esperar a que las ventanas de edición y lectura terminen
        time.sleep(0.1)
    texto_Ventana.delete('1.0', 'end')
    texto_Ventana.insert('end', "Guardando...")
    texto_Ventana.update()
    time.sleep(2)
    texto_Ventana.delete('1.0', 'end')
    texto_Ventana.insert('end', "Guardado completado.")
    texto_Ventana.update()
    edicion_Semaforo.release()
    archivo_Semaforo.release()

def lectura_concurrente():
    while archivo_Semaforo._value == 0:
        time.sleep(0.1)

def ventana(ventana_id):
    root = tk.Tk()
    root.title(f"Ventana {ventana_id}")
    texto_Ventana = tk.Text(root, wrap=tk.WORD)
    texto_Ventana.pack()

    boton_Leer = tk.Button(root, text="Leer", state=tk.NORMAL)
    boton_Editar = tk.Button(root, text="Editar")
    boton_Guardar = tk.Button(root, text="Guardar")

    boton_Leer.pack()
    boton_Editar.pack()
    boton_Guardar.pack()

    # Agregar evento para iniciar la simulación de escritura
    boton_Editar.config(command=lambda: simular_escritura(ventana_id, texto_Ventana))
    boton_Guardar.config(command=lambda: guardar_archivo(ventana_id, texto_Ventana))
    boton_Leer.config(command=lambda: leer_archivo(ventana_id, texto_Ventana))
    
    root.mainloop()

thread1 = threading.Thread(target=ventana, args=(1,))
thread2 = threading.Thread(target=ventana, args=(2,))
thread3 = threading.Thread(target=ventana, args=(3,))

thread1.start()
thread2.start()
thread3.start()
