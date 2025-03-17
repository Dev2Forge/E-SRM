"""AUTHOR + INFO
    Effect Screen Recorder Master (ESRM), es un programa que le permitirá grabar su pantalla y sin necesidad de editores externos,
    podrá agregarle efectos al vídeo final sin postprocesamiento.

    AUTORES:
        - Codificador: Chat GPT :/
        - Idea + Seguimiento: Tutos Rive
    
    VERSIONES:
        - `0.1.0`: Primera versión beta
"""

import json
import customtkinter as ctk
import subprocess
from datetime import datetime
import os
import threading
import queue
import sys

from config_manager import load_config, save_config, DEFAULT_CONFIG
from preview_manager import apply_filters, cover_image

from PIL import Image, ImageFilter, ImageEnhance

class ScreenRecorderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Effect Screen Recorder Master (ESRM) - TRG x CHATGPT")
        self.geometry("1000x600")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        
        self.recording_process = None
        self.config_file = f"{os.path.dirname(os.path.abspath(__file__))}\\config.json"
        self.audio_devices = []
        self.log_queue = queue.Queue()
        self.stop_event = threading.Event()
        
        self.is_recording = False
        self.output_path = ""
        
        self.defaults = DEFAULT_CONFIG.copy()
        self.cover_ratio = 1.0  # Contenedor cuadrado 1:1
        
        self.config = load_config(self.config_file)
        self.load_audio_devices()
        self.create_widgets()
        self.bind("<Configure>", self.on_resize_window)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.after(100, self.process_log_queue)

    def load_audio_devices(self):
        try:
            result = subprocess.run(
                ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            lines = result.stderr.split('\n')
            self.audio_devices = [line.split('"')[1] for line in lines if 'audio' in line and '"' in line]
        except Exception as e:
            self.show_error(f"Error detectando dispositivos: {e}")

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Row 0: Título y Estado
        self.title_label = ctk.CTkLabel(self.main_frame, text="Configuración de Grabación", font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.status_label = ctk.CTkLabel(self.main_frame, text="No grabando", font=("Arial", 14, "bold"))
        self.status_label.grid(row=0, column=1, sticky="e", padx=10)

        # Row 1: Ruta y Dispositivo/Presets
        ruta_frame = ctk.CTkFrame(self.main_frame)
        ruta_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        ruta_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(ruta_frame, text="Ruta de guardado:").grid(row=0, column=0, sticky="w", padx=5)
        self.path_entry = ctk.CTkEntry(ruta_frame)
        self.path_entry.insert(0, self.config.get("output_path", os.path.expanduser("~\\Documents")))
        self.path_entry.grid(row=0, column=1, sticky="ew", padx=5)
        exam_btn = ctk.CTkButton(ruta_frame, text="Examinar...", command=self.on_browse_directory)
        exam_btn.grid(row=0, column=2, padx=5)

        device_frame = ctk.CTkFrame(self.main_frame)
        device_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        device_frame.grid_columnconfigure((0,1,2,3), weight=1)
        ctk.CTkLabel(device_frame, text="Dispositivo:").grid(row=0, column=0, sticky="e", padx=(5,0))
        self.audio_combo = ctk.CTkComboBox(device_frame, values=self.audio_devices, width=120)
        if self.audio_devices:
            self.audio_combo.set(self.config.get("audio_device", self.audio_devices[0]))
        self.audio_combo.grid(row=0, column=1, sticky="w", padx=(0,5))
        ctk.CTkLabel(device_frame, text="Preset:").grid(row=0, column=2, sticky="e", padx=(5,0))
        self.preset_combobox = ctk.CTkComboBox(device_frame, values=["ultrafast","superfast","veryfast","faster","fast","medium"], width=120)
        self.preset_combobox.set(self.config.get("preset", "medium"))
        self.preset_combobox.grid(row=0, column=3, sticky="w", padx=(0,5))

        # Row 2: Efectos y Contenedor Cover (Vista Previa)
        self.effects_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Efectos FFmpeg")
        self.effects_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.effects_frame.grid_columnconfigure(0, weight=1)

        self.cover_container = ctk.CTkFrame(self.main_frame, corner_radius=5)
        self.cover_container.pack_propagate(False)
        self.cover_container.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.select_preview_button = ctk.CTkButton(self.cover_container, text="Seleccionar Preview", command=self.on_select_preview_file)
        self.select_preview_button.pack(side="top", pady=5, padx=10)
        self.preview_label = ctk.CTkLabel(self.cover_container, text="Sin vista previa")
        self.preview_label.pack(side="top", fill="both", expand=True)

        self.brightness = ctk.DoubleVar(value=self.config.get("brightness", self.defaults["brightness"]))
        self.contrast = ctk.DoubleVar(value=self.config.get("contrast", self.defaults["contrast"]))
        self.saturation = ctk.DoubleVar(value=self.config.get("saturation", self.defaults["saturation"]))
        self.gamma = ctk.DoubleVar(value=self.config.get("gamma", self.defaults["gamma"]))
        self.hue = ctk.DoubleVar(value=self.config.get("hue", self.defaults["hue"]))
        self.sharpness = ctk.DoubleVar(value=self.config.get("sharpness", self.defaults["sharpness"]))

        self.create_effect_slider("Brillo", self.brightness, -1.0, 1.0, "brightness")
        self.create_effect_slider("Contraste", self.contrast, 0.0, 2.0, "contrast")
        self.create_effect_slider("Saturación", self.saturation, 0.0, 3.0, "saturation")
        self.create_effect_slider("Gamma", self.gamma, 0.1, 3.0, "gamma")
        self.create_effect_slider("Hue", self.hue, -180.0, 180.0, "hue")
        self.create_effect_slider("Nitidez", self.sharpness, 0.0, 2.0, "sharpness")

        self.original_image = None
        preview_path = self.config.get("preview_path", "")
        if preview_path and os.path.exists(preview_path):
            self.load_preview_image(preview_path)
        else:
            if os.path.exists("assets/preview.png"):
                self.load_preview_image("assets/preview.png")
                self.config["preview_path"] = "assets/preview.png"
                save_config(self.config_file, self.config)
            else:
                self.log("No se ha seleccionado una imagen de vista previa.")

        self.record_button = ctk.CTkButton(self.main_frame, text="Iniciar Grabación", command=self.toggle_recording, fg_color="#2AAA8A", hover_color="#228B22", font=("Arial", 12, "bold"), height=40, width=150)
        self.record_button.grid(row=3, column=0, columnspan=2, sticky="n", pady=5)

    def on_resize_window(self, event):
        if event.widget == self:
            self.adjust_cover_container()

    def adjust_cover_container(self):
        total_width = self.main_frame.winfo_width()
        total_height = self.main_frame.winfo_height()
        container_w = int(total_width * 0.45)
        container_h = container_w  # Cuadrado 1:1
        max_height = total_height - 150
        if container_h > max_height:
            container_h = max_height
            container_w = container_h
        self.cover_container.configure(width=container_w, height=container_h)
        self.update_preview()

    def create_effect_slider(self, label_text, var, min_val, max_val, key_name):
        row_index = len(self.effects_frame.grid_slaves())
        label = ctk.CTkLabel(self.effects_frame, text=label_text + ":")
        label.grid(row=row_index, column=0, sticky="w", padx=5, pady=(5,0))
        slider = ctk.CTkSlider(self.effects_frame, from_=min_val, to=max_val, variable=var, number_of_steps=100, command=self.update_preview)
        slider.grid(row=row_index+1, column=0, sticky="ew", padx=5, pady=(0,5))
        def reset_value():
            default_val = self.defaults[key_name]
            var.set(default_val)
            self.update_preview()
        reset_btn = ctk.CTkButton(self.effects_frame, text="Reset", width=60, command=reset_value)
        reset_btn.grid(row=row_index+1, column=1, padx=5, pady=(0,5), sticky="e")

    def on_browse_directory(self):
        selected_dir = ctk.filedialog.askdirectory()
        if selected_dir:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, selected_dir)

    def on_select_preview_file(self):
        filetypes = [("Imágenes", "*.png *.jpg *.jpeg *.gif"), ("Todos los archivos", "*.*")]
        selected = ctk.filedialog.askopenfilename(filetypes=filetypes)
        if not selected:
            return
        ext = os.path.splitext(selected)[1].lower()
        if ext in [".png", ".jpg", ".jpeg", ".gif"]:
            self.load_preview_image(selected)
            self.config["preview_path"] = selected
            save_config(self.config_file, self.config)
        else:
            self.show_error("No se admite video en la vista previa por ahora.")

    def load_preview_image(self, path):
        try:
            img = Image.open(path)
            if getattr(img, "is_animated", False):
                img.seek(0)
            img = img.convert("RGBA")
            self.original_image = img
            self.update_preview()
        except Exception as e:
            self.show_error(f"No se pudo cargar la imagen: {e}")

    def update_preview(self, *args):
        if not self.original_image:
            return
        preview_img = self.original_image.copy()
        unsharp_factor = self.sharpness.get()
        unsharp_mask = ImageFilter.UnsharpMask(radius=2, percent=int((unsharp_factor - 1.0) * 150 + 100), threshold=3)
        preview_img = preview_img.filter(unsharp_mask)
        brightness_factor = 1.0 + self.brightness.get()
        preview_img = ImageEnhance.Brightness(preview_img).enhance(brightness_factor)
        contrast_factor = self.contrast.get()
        preview_img = ImageEnhance.Contrast(preview_img).enhance(contrast_factor)
        saturation_factor = self.saturation.get()
        preview_img = ImageEnhance.Color(preview_img).enhance(saturation_factor)
        gamma_factor = self.gamma.get()
        if gamma_factor != 1.0:
            from math import pow
            lut = [int(255 * pow((i/255), 1/gamma_factor)) for i in range(256)]
            num_channels = len(preview_img.getbands())
            preview_img = preview_img.point(lut * num_channels)
        hue_shift = self.hue.get()
        if hue_shift != 0:
            preview_img = preview_img.convert("HSV")
            hdata = list(preview_img.getdata())
            new_data = []
            for h, s, v in hdata:
                hd = (h * 360.0 / 255.0 + hue_shift) % 360
                new_data.append((int(hd / 360.0 * 255), s, v))
            preview_img.putdata(new_data)
            preview_img = preview_img.convert("RGBA")
        
        # Lógica "cover" para que la imagen llene todo el contenedor (cover_container) (1:1)
        container_w = self.cover_container.winfo_width()
        container_h = self.cover_container.winfo_height()
        if container_w < 10 or container_h < 10:
            container_w, container_h = 600, 600
        # Usamos la función cover_image del módulo preview_manager para obtener el efecto "cover"
        preview_img = cover_image(preview_img, container_w, container_h)
        
        self.preview_ctkimage = ctk.CTkImage(light_image=preview_img, size=(container_w, container_h))
        self.preview_label.configure(image=self.preview_ctkimage, text="")

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        try:
            output_dir = self.path_entry.get()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"grabacion_{timestamp}.mp4"
            self.output_path = os.path.join(output_dir, output_file)
            ff_brightness = self.brightness.get()
            ff_contrast = self.contrast.get()
            ff_saturation = self.saturation.get()
            ff_gamma = self.gamma.get()
            ff_hue = self.hue.get()
            ff_sharp = self.sharpness.get()
            filter_chain = (
                f"unsharp=lx=5:ly=5:la={ff_sharp:.1f},"
                f"eq=brightness={ff_brightness:.2f}:contrast={ff_contrast:.2f}"
                f":saturation={ff_saturation:.2f}:gamma={ff_gamma:.2f},"
                f"hue=h={ff_hue:.2f}"
            )
            command = [
                'ffmpeg',
                '-y',
                '-f', 'gdigrab',
                '-framerate', '30',
                '-i', 'desktop',
                '-f', 'dshow',
                '-i', f'audio={self.audio_combo.get().strip()}',
                '-vf', filter_chain,
                '-c:v', 'libx264',
                '-preset', self.preset_combobox.get(),
                '-pix_fmt', 'yuv420p',
                '-crf', '18',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-strict', 'experimental',
                self.output_path
            ]
            self.recording_process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.is_recording = True
            self.record_button.configure(
                text="Detener Grabación",
                fg_color="#FF6347",
                hover_color="#CD5555"
            )
            self.status_label.configure(text="Grabando...")
            self.monitor_thread = threading.Thread(target=self.read_process_output, daemon=True)
            self.stop_event.clear()
            self.monitor_thread.start()
        except Exception as e:
            self.show_error(f"Error al iniciar grabación: {e}")
            self.stop_recording()

    def read_process_output(self):
        while self.is_recording and not self.stop_event.is_set():
            line = self.recording_process.stdout.readline()
            if not line:
                break
        if self.recording_process.poll() is not None:
            self.stop_recording()

    def stop_recording(self):
        if self.recording_process and self.is_recording:
            try:
                self.stop_event.set()
                self.recording_process.communicate(input='q\n', timeout=5)
            except subprocess.TimeoutExpired:
                self.recording_process.terminate()
            finally:
                self.recording_process = None
                self.is_recording = False
                self.record_button.configure(
                    text="Iniciar Grabación",
                    fg_color="#2AAA8A",
                    hover_color="#228B22"
                )
                self.status_label.configure(text="No grabando")
                save_config(self.config_file, self.config)

    def log(self, message):
        print(message)

    def show_error(self, message):
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("450x200")
        error_dialog.transient(self)
        error_dialog.grab_set()
        ctk.CTkLabel(error_dialog, text=message, wraplength=400, font=("Arial", 12)).pack(pady=20, padx=20)
        ctk.CTkButton(error_dialog, text="OK", command=error_dialog.destroy, width=100).pack(pady=10)

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = DEFAULT_CONFIG.copy()
        except Exception as e:
            self.show_error(f"Error cargando configuración: {e}")
            self.config = DEFAULT_CONFIG.copy()

    def save_config(self):
        try:
            self.config.update({
                "output_path": self.path_entry.get(),
                "audio_device": self.audio_combo.get(),
                "preset": self.preset_combobox.get(),
                "brightness": self.brightness.get(),
                "contrast": self.contrast.get(),
                "saturation": self.saturation.get(),
                "gamma": self.gamma.get(),
                "hue": self.hue.get(),
                "sharpness": self.sharpness.get()
            })
            save_config(self.config_file, self.config)
        except Exception as e:
            self.show_error(f"Error guardando configuración: {e}")

    def process_log_queue(self):
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.log(message)
        self.after(100, self.process_log_queue)

    def on_closing(self):
        if self.is_recording:
            self.stop_recording()
        self.save_config()
        self.destroy()


if __name__ == "__main__":
    app = ScreenRecorderApp()

    def custom_excepthook(exctype, value, tb):
        if app.is_recording:
            app.stop_recording()
        sys.__excepthook__(exctype, value, tb)

    sys.excepthook = custom_excepthook

    app.mainloop()
