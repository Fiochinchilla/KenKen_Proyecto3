import tkinter as tk
from tkinter import messagebox

############################# Inica Funcion de Ventana Principal #######################################
def ventana_principal():
    global ventana
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Mi Aplicación")

    # Crear el menú de opciones
    menu = tk.Menu(ventana)

    # Agregar las opciones al menú
    menu.add_command(label="Jugar", command=jugar)
    menu.add_command(label="Configurar", command=configuracion)
    menu.add_command(label="Ayuda", command=ayuda)
    menu.add_command(label="Acerca de", command=acerca_de)
    menu.add_command(label="Salir", command=salir)

    # Configurar la ventana para usar el menú
    ventana.config(menu=menu)

    # Iniciar la aplicación
    ventana.mainloop()




################################# Inicia Funciones para Jugar ###############################################
def jugar():
    # Agrega aquí la lógica para la opción "Jugar"
    messagebox.showinfo("Jugar", "¡Comienza el juego!")







################################# Inicia Funciones para Configuracion ###############################################
def guardar_configuracion():
    with open('kenken_configuracion.dat', 'w') as archivo:
            archivo.write(f"{dificultad.get()}\n")
            archivo.write(f"{reloj.get()}\n")
            archivo.write(f"{posicion_panel.get()}\n")
            archivo.write(f"{sonido.get()}\n")
    archivo.close()
    messagebox.showinfo("Éxito", "Los datos se han guardado correctamente.")
            

def configuracion():
    global dificultad, reloj, posicion_panel, sonido

    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Configuración KenKen")

    # Variables para los datos
    dificultad = tk.StringVar()
    reloj = tk.StringVar()
    posicion_panel = tk.StringVar()
    sonido = tk.StringVar()

    # Asignar valores iniciales a las variables
    dificultad.set("Facil")  # Establece "Facil" como valor inicial
    reloj.set("Cronometro")  # Establece "Cronometro" como valor inicial
    posicion_panel.set("Derecha")  # Establece "Derecha" como valor inicial
    sonido.set("Si")  # Establece "Si" como valor inicial

    # Formato de fuente
    formato_texto = ("Arial", 15)

    # Configuración de la dificultad
    frame_dificultad = tk.Frame(ventana)
    frame_dificultad.pack()
    tk.Label(frame_dificultad, text="Dificultad:", font=formato_texto).pack()
    dificultad_options = ["Facil", "Intermedio", "Dificil"]
    for option in dificultad_options:
        tk.Radiobutton(frame_dificultad, text=option, variable=dificultad, value=option, font=formato_texto).pack()

    # Configuración del reloj
    frame_reloj = tk.Frame(ventana)
    frame_reloj.pack()
    tk.Label(frame_reloj, text="Reloj:", font=formato_texto).pack()
    reloj_options = ["Cronometro", "No", "Timer"]
    for option in reloj_options:
        tk.Radiobutton(frame_reloj, text=option, variable=reloj, value=option, font=formato_texto).pack()

    # Configuración de la posición del panel
    frame_posicion_panel = tk.Frame(ventana)
    frame_posicion_panel.pack()
    tk.Label(frame_posicion_panel, text="Posición del panel:", font=formato_texto).pack()
    tk.Radiobutton(frame_posicion_panel, text="Derecha", variable=posicion_panel, value="Derecha", font=formato_texto).pack()
    tk.Radiobutton(frame_posicion_panel, text="Izquierdo", variable=posicion_panel, value="Izquierdo", font=formato_texto).pack()

    # Configuración del sonido
    frame_sonido = tk.Frame(ventana)
    frame_sonido.pack()
    tk.Label(frame_sonido, text="Sonido:", font=formato_texto).pack()
    tk.Radiobutton(frame_sonido, text="Si", variable=sonido, value="Si", font=formato_texto).pack()
    tk.Radiobutton(frame_sonido, text="No", variable=sonido, value="No", font=formato_texto).pack()

    # Botón para guardar configuración
    boton_guardar = tk.Button(ventana, text="Guardar Configuración", command=guardar_configuracion, font=formato_texto)
    boton_guardar.pack()

    ventana.mainloop()











################################# Inicia Funciones para Ayuda ###############################################
def ayuda():
    # Agrega aquí la lógica para la opción "Ayuda"
    messagebox.showinfo("Ayuda", "¡Obtén ayuda aquí!")


################################# Inicia Funciones para Acerca de ###############################################
def acerca_de():
    # Agrega aquí la lógica para la opción "Acerca de"
    messagebox.showinfo("Acerca de", "Aplicación creada por [Tu Nombre]")

################################# Inicia Funciones para Salir ###############################################

def salir():
    ventana.quit()



ventana_principal()