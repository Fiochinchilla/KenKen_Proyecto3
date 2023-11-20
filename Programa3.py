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
    menu.add_command(label="Jugar", command=crear_ventana)
    menu.add_command(label="Configurar", command=configuracion)
    menu.add_command(label="Ayuda", command=ayuda)
    menu.add_command(label="Acerca de", command=acerca_de)
    menu.add_command(label="Salir", command=salir)

    # Configurar la ventana para usar el menú
    ventana.config(menu=menu)

    # Iniciar la aplicación
    ventana.mainloop()


################################# Inicia Funciones para Jugar ###############################################
def obtener_configuracion():
    try:
        with open('kenken_configuracion.dat', 'r') as file:
            lineas = file.readlines()
            return [linea.strip() for linea in lineas]
    except FileNotFoundError:
        return None


#Funcion para resaltar la casilla seleccionada de color celeste
def seleccionar_casilla(coord):
    global coordenada_seleccionada
    coordenada_seleccionada = coord
    for entry_coord, entry_widget in entries.items():
        if entry_coord == coord:
            entry_widget.config(bg="lightblue") #Resalta la casilla seleccionada de color celeste
            
        else:
            entry_widget.config(bg="white")

#Funcion para colocar uno de los numeros de los botones en la casilla seleccionada
def colocar_numero(numero):
    global coordenada_seleccionada
    if coordenada_seleccionada:
        # Obtiene la entrada seleccionada
        entry = entries[coordenada_seleccionada]
        entry.num_label.config(text=str(numero))
        # Obtiene las coordenadas de la entrada
        row, col = coordenada_seleccionada
        # Guarda el número en la pila correspondiente a esa casilla
        stacks[row][col].append(numero)


#Funcion para crear el tablero, y los botones de numeros y de opciones
def iniciar_juego(contenido):
    global root
    
    root = tk.Tk()
    root.title("KenKen")

    frame_principal = tk.Frame(root)
    frame_principal.pack()

    frame_tablero = tk.Frame(frame_principal)
    frame_tablero.grid(row=0, column=1, padx=20, pady=20)

    # Crear el frame para los botones de números (1-6)
    frame_numeros = tk.Frame(frame_principal)
    frame_numeros.grid(row=0, column=2, padx=20, pady=20)

    # Crear el frame para los botones de juego debajo del tablero
    frame_botones_juego = tk.Frame(frame_principal)
    frame_botones_juego.grid(row=1, column=0, columnspan=2, pady=10)

    operaciones = contenido[1:] #Leer el contenido de los juegos sin contar el primer dato (F, M, D)

    tamaño_celda = 80  # Tamaño deseado de la celda
    fuente_operaciones = ("Arial", 10)  # Fuente y tamaño de la operación

    global entries  # Referencia global para almacenar las casillas

    entries = {}  # Diccionario para almacenar las referencias a las etiquetas de las casillas

    for i in range(6):
        for j in range(6):
            frame_celda = tk.Frame(frame_tablero, width=tamaño_celda, height=tamaño_celda, bd=1, relief=tk.SOLID)
            frame_celda.grid(row=i, column=j)
            coord = (i, j)
            entries[coord] = frame_celda

            label_operacion = tk.Label(frame_celda, font=fuente_operaciones)
            label_operacion.place(x=5, y=5)  # Posición en la esquina superior izquierda

            label_numero = tk.Label(frame_celda, font=("Arial", 16))
            label_numero.place(relx=0.5, rely=0.5, anchor='center')
            frame_celda.num_label = label_numero

            # Asignar evento de clic para seleccionar la casilla
            frame_celda.bind("<Button-1>", lambda event, coord=coord: seleccionar_casilla(coord))

    # Botones numéricos (1-6) organizados verticalmente
    for i in range(1, 7):
        btn_numero = tk.Button(frame_numeros, text=str(i), width=4, height=2,
                               font=("Arial", 12), command=lambda num=i: colocar_numero(num))
        btn_numero.grid(row=i-1, column=0, padx=5, pady=5)

    for op in operaciones:
        operation, *coords = op
        row, col = coords[0][0] - 1, coords[0][1] - 1  # Ajustar las coordenadas
        frame_celda = entries[(row, col)]  # Obtener la celda correspondiente
        frame_celda.children['!label'].config(text=operation)
    
    frame_principal.grid_rowconfigure(0, weight=1)
    frame_principal.grid_rowconfigure(1, weight=1)
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)

    configuracion = obtener_configuracion()  # Función para obtener la configuración del archivo

    tipo_contador = configuracion[1]
    posicion_contador = configuracion[2]

    #Determianr si es con cronometro o con temporizador
    if tipo_contador == "Cronometro":
        mostrar_cronometro(frame_tablero, posicion_contador)  
    elif tipo_contador == "Temporizador":
        mostrar_temporizador(frame_tablero, posicion_contador)  
    else:
        pass

    # Botones de juego debajo del tablero
    botones_juego = [
        ("Iniciar Juego",print("Iniciar Juego")),
        ("Validar Juego", print("Validar Juego")),
        ("Deshacer Jugada", deshacer_jugada),
        ("Otro Juego", print("Otro Juego")),
        ("Terminar Juego", terminar_juego),
        ("Reiniciar Juego", reiniciar_juego),
        ("Top 10", lambda: print("Top 10")),
    ]

    for nombre, comando in botones_juego:
        boton = tk.Button(frame_botones_juego, text=nombre, width=12, height=2, font=("Arial", 12), command=comando)
        boton.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()


#Funcion para crear y mostrar el cronometro
def mostrar_cronometro(frame_tablero, posicion):
    global running, hours, minutes, seconds

    # Inicializar variables del cronómetro
    running = False
    hours = 0
    minutes = 0
    seconds = 0

    # Crear marco para el cronómetro dentro del marco del tablero
    frame_cronometro = tk.Frame(frame_tablero)
    frame_cronometro.grid(row=1, column=0, columnspan=6, padx=20, pady=10)

    # Configurar etiqueta para mostrar el tiempo
    timer_label = tk.Label(frame_cronometro, text="00:00:00", font=("Helvetica", 24))
    timer_label.pack()

    # Funciones del cronómetro
    def iniciar_cronometro():
        global running
        running = True
        actualizar_cronometro()

    def detener_cronometro():
        global running
        running = False

    def reiniciar_cronometro():
        global running, hours, minutes, seconds
        running = False
        hours = 0
        minutes = 0
        seconds = 0
        timer_label.config(text="00:00:00")

    def actualizar_cronometro():
        global running, hours, minutes, seconds
        if running:
            seconds += 1
            if seconds == 60:
                seconds = 0
                minutes += 1
                if minutes == 60:
                    minutes = 0
                    hours += 1
            timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            timer_label.after(1000, actualizar_cronometro)

    # Botones de control del cronómetro
    start_button = tk.Button(frame_cronometro, text="Iniciar", command=iniciar_cronometro)
    stop_button = tk.Button(frame_cronometro, text="Detener", command=detener_cronometro)
    reset_button = tk.Button(frame_cronometro, text="Reiniciar", command=reiniciar_cronometro)

    start_button.pack(side=tk.LEFT, padx=5)
    stop_button.pack(side=tk.LEFT, padx=5)
    reset_button.pack(side=tk.LEFT, padx=5)

    # Ajustar posición según configuración
    if posicion == "Derecha":
        frame_cronometro.grid(row=1, column=6, padx=20, pady=10)  # Posición a la derecha
    else:
        frame_cronometro.grid(row=1, column=0, padx=20, pady=10)


#Funcion en la que se encuentra l alogica del temporizador
def iniciar_temporizador(horas_var, minutos_var, segundos_var, tiempo_label):
    horas = int(horas_entry.get())
    minutos = int(minutos_entry.get())
    segundos = int(segundos_entry.get())

    tiempo_total = horas * 3600 + minutos * 60 + segundos

    def actualizar_temporizador():
        nonlocal tiempo_total
        if tiempo_total > 0:
            tiempo_total -= 1
            horas = tiempo_total // 3600
            minutos = (tiempo_total % 3600) // 60
            segundos = tiempo_total % 60

            tiempo_str = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            tiempo_label.config(text=tiempo_str)
            tiempo_label.after(1000, actualizar_temporizador)
        else:
            messagebox.showinfo("Fin del temporizador", "El temporizador ha terminado")

    actualizar_temporizador()

#Funcion para poder mostrar el temporizador en la ventana 
def mostrar_temporizador(frame_tablero, posicion):
    global horas_entry, minutos_entry, segundos_entry
    frame_temporizador = tk.Frame(frame_tablero)

    horas_var = tk.StringVar()
    minutos_var = tk.StringVar()
    segundos_var = tk.StringVar()

    horas_label = tk.Label(frame_temporizador, text="Horas:")
    horas_label.grid(row=0, column=0)
    horas_entry = tk.Entry(frame_temporizador, textvariable=horas_var)
    horas_entry.grid(row=0, column=1)

    minutos_label = tk.Label(frame_temporizador, text="Minutos:")
    minutos_label.grid(row=1, column=0)
    minutos_entry = tk.Entry(frame_temporizador, textvariable=minutos_var)
    minutos_entry.grid(row=1, column=1)

    segundos_label = tk.Label(frame_temporizador, text="Segundos:")
    segundos_label.grid(row=2, column=0)
    segundos_entry = tk.Entry(frame_temporizador, textvariable=segundos_var)
    segundos_entry.grid(row=2, column=1)

    tiempo_label = tk.Label(frame_temporizador, text="00:00:00", font=("Arial", 18))
    tiempo_label.grid(row=4, columnspan=2)

    iniciar_button = tk.Button(frame_temporizador, text="Iniciar", command=lambda: iniciar_temporizador(horas_var, minutos_var, segundos_var, tiempo_label))
    iniciar_button.grid(row=3, columnspan=2)

    # Ajustar posición según configuración
    if posicion == "Derecha":
        frame_temporizador.grid(row=2, column=6, padx=20, pady=10)  # Posición a la derecha
    else:
        frame_temporizador.grid(row=2, column=0, padx=3, pady=10, sticky='w')


#Funcion correspondiente al boton "Deshacer Jugada"
def deshacer_jugada():
    global coordenada_seleccionada
    if coordenada_seleccionada:
        row, col = coordenada_seleccionada
        # Verifica si hay elementos en la pila para esa casilla
        if stacks[row][col]:
            # Elimina el último número colocado y lo muestra en la entrada
            numero_anterior = stacks[row][col].pop()
            entry = entries[coordenada_seleccionada]
            entry.num_label.config(text=str(numero_anterior))

#Funcion para reiniciar el tablero del juego:
def reiniciar_juego():
    # Función que se ejecuta al presionar el botón "Reiniciar Juego"
    def confirmar_reinicio():
        # Función para mostrar el cuadro de diálogo de confirmación
        respuesta = messagebox.askyesno("Reiniciar Juego", "¿Estás seguro que deseas reiniciar el juego?")
        if respuesta:  # Si se presiona "Sí"
            # Recorre todas las entradas del tablero y restablece sus valores a cero
            for row in range(6):
                for col in range(6):
                    entry = entries[(row, col)]
                    entry.num_label.config(text="")  # Borra el número mostrado
                    # Limpia la pila de esa casilla para reiniciar el juego
                    stacks[row][col] = []

    # Llama a la función de confirmación para mostrar el cuadro de diálogo
    confirmar_reinicio()

#Crear la ventana para el juego
def crear_ventana():
    def on_iniciar_juego_click():
        global nombre_usuario
        nombre = entry_nombre.get().strip()

        if nombre:  # Verificar si se ingresó un nombre
            nombre_usuario = nombre
            iniciar_juego(contenido)
            ventana_nombre.destroy()  # Cerrar ventana del nombre
        else:
            lbl_error.config(text="Por favor, ingresa tu nombre", fg="red")  # Mostrar mensaje de error

    ventana_nombre = tk.Tk()
    ventana_nombre.title("Nombre de Usuario")

    frame_principal = tk.Frame(ventana_nombre)
    frame_principal.pack()

    label_nombre = tk.Label(frame_principal, text="Nombre del jugador:")
    label_nombre.pack()

    entry_nombre = tk.Entry(frame_principal, font=("Arial", 12))
    entry_nombre.pack()

    lbl_error = tk.Label(frame_principal, text="", fg="red")
    lbl_error.pack()

    # Botón para iniciar juego centrado en la pantalla
    btn_iniciar = tk.Button(frame_principal, text="Iniciar juego", width=12, height=2, font=("Arial", 12),
                            command=on_iniciar_juego_click)
    btn_iniciar.pack()

    ventana_nombre.mainloop()

    
#Funcion para terminar el juego
def terminar_juego():
    # Función que se ejecuta al presionar el botón "Terminar Juego"
    def confirmar_terminar():
        # Función para mostrar el cuadro de diálogo de confirmación
        respuesta = messagebox.askyesno("Terminar Juego", "¿Estás seguro que deseas terminar el juego?")
        if respuesta:  # Si se presiona "Sí"
            root.destroy()  # Cierra la ventana principal del juego

    # Llama a la función de confirmación para mostrar el cuadro de diálogo
    confirmar_terminar()







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
    ventana_acerca_de = tk.Toplevel()  
    ventana_acerca_de.title("Acerca de")

    info_text = """
    Escuela de Computación Carrera: Ingeniería en Computación
    Curso: Taller de Programación

    Tercer Proyecto Programado
    KenKen

    Estudiantes:
    Adolfo Barquero 2022211388
    Fiorella Chinchilla 2023800072

    Profesor:
    William Mata

    II Semestre 2023
    """

    # Crear una etiqueta para mostrar la información
    info_label = tk.Label(ventana_acerca_de, text=info_text, font=("Arial", 12))
    info_label.pack(padx=20, pady=20)

    


################################# Inicia Funciones para Salir ###############################################

def salir():
    ventana.quit()


#Abrir y guardar los datos del archivo de configuracion
archivo = "kenken_juegos.dat"
with open(archivo, "r") as file:
    contenido = eval(file.read().replace("\\n", ""))

#Variables Globales
selected_entry = None
entries = {}  # Diccionario para almacenar los entries
operaciones = []  # Lista para almacenar las operaciones
nombre_jugador = ""


#Pilas para almacenar los datos colocados en cada una de las casillas
stacks = [[[] for _ in range(6)] for _ in range(6)]

ventana_principal()
