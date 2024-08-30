import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import pyttsx3
import threading
from tkinter.font import Font, families
import os

class StoryGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Generador de Historias Mágicas")
        master.geometry("900x600")
        master.configure(bg="#2C3E50")  # Fondo oscuro para contraste

        # Cargar la fuente personalizada
        self.load_custom_font()

        # Centrar la ventana en la pantalla
        self.center_window()

        # Inicializar el motor de voz
        self.engine = pyttsx3.init()

        # Configurar fuentes
        default_font = Font(family="Product Sans", size=11)
        title_font = Font(family="Product Sans", size=24, weight="bold")
        button_font = Font(family="Product Sans", size=14, weight="bold")

        # Estilos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Estilo para TFrame
        self.style.configure("Custom.TFrame", 
                             background="#34495E",
                             borderwidth=0,
                             relief="flat")
        
        # Estilo para TButton
        self.style.configure("Custom.TButton", 
                             background="#3498DB", 
                             foreground="white", 
                             font=button_font,
                             padding=10,
                             borderwidth=0,
                             relief="flat",)
        self.style.map("Custom.TButton", 
                       background=[("active", "#2980B9")])
        
        # Estilo para Checkbuttons
        self.style.configure("Custom.TCheckbutton",
                             background="#34495E",
                             foreground="#ECF0F1",
                             font=default_font)
        self.style.map("Custom.TCheckbutton",
                       background=[("active", "#34495E")],
                       foreground=[("active", "#3498DB")])
        
        self.style.configure("Custom.TLabel", 
                             background="#34495E", 
                             foreground="#ECF0F1",
                             font=default_font)

        # Frame principal
        main_frame = ttk.Frame(master, padding="20", style="Custom.TFrame")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título con efecto de sombra
        title_shadow = tk.Label(main_frame, 
                                text="Generador de Historias Mágicas", 
                                font=title_font, 
                                bg="#34495E", 
                                fg="#2C3E50")
        title_shadow.grid(row=0, column=0, pady=(0, 2))
        title = tk.Label(main_frame, 
                         text="Generador de Historias Mágicas", 
                         font=title_font, 
                         bg="#34495E", 
                         fg="#ECF0F1")
        title.grid(row=0, column=0, pady=(0, 5))

        # Frame para opciones
        options_frame = ttk.Frame(main_frame, padding="10", style="Custom.TFrame")
        options_frame.grid(row=1, column=0, pady=10)

        ttk.Label(options_frame, text="Opciones:", style="Custom.TLabel").grid(row=0, column=0, pady=2, sticky="w")

        self.voice_var = tk.IntVar(value=1)
        voice_check = ttk.Checkbutton(options_frame, text="Activar voz", variable=self.voice_var, style="Custom.TCheckbutton")
        voice_check.grid(row=1, column=0, sticky="w", pady=5)

        self.ia_var = tk.IntVar(value=1)
        ia_check = ttk.Checkbutton(options_frame, text="Activar mejora IA", variable=self.ia_var, style="Custom.TCheckbutton")
        ia_check.grid(row=2, column=0, sticky="w", pady=5)

        # Botón para generar la historia
        self.generate_button = ttk.Button(main_frame, text="Generar Historia Mágica", command=self.generate_story, style="Custom.TButton")
        self.generate_button.grid(row=2, column=0, pady=10)

        # Área de texto para mostrar la historia
        self.story_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=12, font=default_font)
        self.story_text.grid(row=3, column=0, pady=10)
        self.story_text.configure(bg="#ECF0F1", fg="#2C3E50")

        # Poner el autor en la parte inferior
        ttk.Label(main_frame, text="Creado por: Williams Chan", style="Custom.TLabel").grid(row=4, column=0, pady=0)


    def load_custom_font(self):
        font_path = "/Font/ProductSans.ttf"  # Reemplaza esto con la ruta real a tu archivo .ttf
        if os.path.exists(font_path):
            self.master.tk.call('font', 'create', 'ProductSans', 
                                '-family', 'Product Sans', 
                                '-file', font_path)
            print("Fuente Product Sans cargada correctamente.")
        else:
            print("No se pudo encontrar el archivo de fuente. Usando fuente predeterminada.")

    def center_window(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def generate_story(self):
        self.generate_button.configure(state="disabled")
        self.story_text.delete('1.0', tk.END)
        self.story_text.insert(tk.END, "Generando tu historia mágica...\n\n")
        
        args = ['python', 'HistoryFinal.py', 
                f'-Voice={self.voice_var.get()}', 
                f'-IA={self.ia_var.get()}']
        
        def run_script():
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate()

            self.master.after(0, self.update_story_text, output, error)

        threading.Thread(target=run_script, daemon=True).start()

    def update_story_text(self, output, error):
        self.story_text.delete('1.0', tk.END)
        if error:
            self.story_text.insert(tk.END, f"Error: {error}")
        else:
            self.story_text.insert(tk.END, output)
            if self.voice_var.get():
                self.master.after(500, lambda: threading.Thread(target=self.read_text_aloud, args=(output,)).start())
        self.generate_button.configure(state="normal")

    def read_text_aloud(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    gui = StoryGeneratorGUI(root)
    root.mainloop()