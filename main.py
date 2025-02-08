import tkinter as tk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi primera ventana")

# Crear un label (etiqueta) con el texto "Hola"
etiqueta = tk.Label(ventana, text="Hola")
etiqueta.pack()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()