import os
import json
import subprocess

# Nombre del proyecto
project_name = "mi_proyecto"

# Carpetas del proyecto
folders = [
    project_name,
    f"{project_name}/.vscode",
]

# Archivos y su contenido
files = {
    f"{project_name}/main.py": """\
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Mi Aplicación en Tkinter")
    root.geometry("400x300")

    label = tk.Label(root, text="¡Hola, mundo!", font=("Arial", 14))
    label.pack(pady=20)

    button = tk.Button(root, text="Cerrar", command=root.quit)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
""",
    f"{project_name}/.vscode/launch.json": json.dumps({
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python Debugger: main.py",
                "type": "debugpy",
                "request": "launch",
                "program": "${workspaceFolder}/main.py",
                "console": "integratedTerminal"
            }
        ]
    }, indent=4)
}

# Crear carpetas
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Crear archivos
for file_path, content in files.items():
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

# Instalar `debugpy` si no está instalado
try:
    import debugpy
except ImportError:
    print("⚠ Instalando debugpy...")
    subprocess.run(["pip", "install", "debugpy"])

# Abrir VS Code en la carpeta del proyecto
print(f"✅ Proyecto '{project_name}' creado con éxito.")
print("📂 Abriendo en VS Code...")
subprocess.run(["code", project_name])
