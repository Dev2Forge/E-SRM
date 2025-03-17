import json
import os

DEFAULT_CONFIG = {
    "output_path": os.path.expanduser("~\\videos"),
    "audio_device": "",
    "preset": "medium",
    "brightness": 0.0,
    "contrast": 1.0,
    "saturation": 1.0,
    "gamma": 1.0,
    "hue": 0.0,
    "sharpness": 1.0,
    "preview_path": f'{os.path.dirname(os.path.abspath(__file__))}\\assets\\preview.png'
}

def load_config(config_file):
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando configuración: {e}")
    return DEFAULT_CONFIG.copy()

def save_config(config_file, config):
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error guardando configuración: {e}")
