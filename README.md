# 🎥 Effect Screen Recorder Master (ESRM) v0.1.0

---

<div style="display: flex; align-items: center; justify-content: center; margin: 10px 0; gap: 10px; max-height: 48px; height: 48px;">
  <a href="https://github.com/sponsors/tutosrive" target="_blank">
  <img src="https://img.shields.io/badge/Sponsor-%F0%9F%92%96%20tutosrive-orange?style=for-the-badge&logo=github" alt="Sponsor me on GitHub">
</a>
  <a href="https://www.buymeacoffee.com/tutosrive">
    <img 
      src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=tutosrive&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" 
      style="height: 48px; width: auto; object-fit: contain; border-radius: 6px;" 
      alt="Buy me a coffee button">
  </a>
</div>

---

<!-- Total downloads -->
[![Total Downloads](https://static.pepy.tech/badge/effect-srm)](https://pepy.tech/projects/effect-srm)
[![Python 3.11.6+](https://img.shields.io/badge/Python-3.11.6%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FFmpeg Required](https://img.shields.io/badge/FFmpeg-Required-orange.svg)](https://ffmpeg.org/)
[![Effect Screen Recorder Master - Version](https://img.shields.io/pypi/v/effect-srm?label=ESRM)](https://pypi.org/project/effect-srm)
[![Author](https://img.shields.io/badge/Tutos%20Rive-Author-brightgreen)](https://github.com/tutosrive)

```shell
# Ejecutar en CMD u otra terminal
pip install effect-srm
```

---

ESRM es un programa para grabación de pantalla con **efectos visuales en tiempo real**, hecho 100% con **chat GPT**, está escrito en **python** y con interfaz gráfica en _Custom Tkinter_, se usa FFMPEG para realizar las grabaciones (en cualquier caso, debe instalar **FFMPEG** y añadirlo al **PATH**).

[![Download effect-screen-recorder-master](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/e-srm/files/latest/download)

```shell
# Ejecutar en CMD u otra terminal
pip install effect-srm
```

Una vez instalado, puede ejecutar uno de los siguientes comandos en una terminal (recuerde, debe tener python instalado)

```shell
# Primer comando
esrm
```
```shell
# Segundo comando
srm
```
```shell
# Tercer comando
effect-screen-recorder-master
```

## **Archivos/Versiones/builds**:

Descargue e instale sin necesidad de tener python instalado [Releases](https://github.com/tutosrive/effect-screen-recorder-master/releases)

## 📦 Requisitos

### Componentes Requeridos
- FFmpeg ([Descarga Directa](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z)) en PATH
- Python 3.11.6 o superior
- Sistema operativo **_probado_**: **Windows 10**

# Interfaz del programa

![Interfaz Principal](https://cdn.jsdelivr.net/gh/tutosrive/images-projects-srm-trg@main/esrm/esrm.png)

## 🌟 Características Principales

### 🎚️ Ajustes en Tiempo Real
- Brillo | Contraste | Saturación | Gamma | Tono | Nitidez
- 6 controles deslizantes con precisión decimal
- Valores por defecto optimizados

### 🖥️ Vista Previa Avanzada
- Panel interactivo 1:1
- Efectos aplicados en tiempo real
- Soporte para imágenes/GIF como vista previa (Ver efectos aplicados)
- Sistema de recorte inteligente (modo cover)

### ⚙️ Configuración Profesional
- Detección automática de dispositivos de audio (micrófono)
- Presets de codificación FFmpeg (`ultrafast` a `medium`)
- Guardado automático de ajustes en **JSON**
- Interfaz oscura moderna con **CustomTKinter**

## 🚀 Instalación Rápida (local)

1. Clonar repositorio:
```bash
git clone https://github.com/tutosrive/effect-screen-recorder-master.git
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar aplicación:
```bash
python code/__main__.py
```

## ⚡ Uso Básico

1. Seleccionar directorio de salida
2. Elegir dispositivo de audio (Es obligatorio, si no se selcciona no grabará...)
3. Ajustar efectos visuales
4. Iniciar grabación con un clic
5. Detener grabación (archivo se guarda automáticamente)

```python
# Estructura de archivo de configuración
{
  "output_path": "C:\\Users\\Usuario\\Videos",
  "audio_device": "Micrófono (Dispositivo HD)",
  "preset": "fast",
  "brightness": 0.2,
  "contrast": 1.1,
  "saturation": 1.3,
  "gamma": 1.0,
  "hue": 0.0,
  "sharpness": 1.5
}
```

## 📄 Licencia

Este proyecto está bajo licencia MIT - ver el archivo [LICENSE](https://github.com/tutosrive/effect-screen-recorder-master/blob/main/LICENSE) para más detalles.

**Atribución Requerida:**
```text
Incluir en todos los usos/modificaciones:
"Effect Screen Recorder Master (ESRM) v0.1.0 © 2025 Tutos Rive - Licencia MIT"
```

## 🤝 Contribución

1. Haz fork del proyecto
2. Crea tu branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Add nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📧 Contacto

**Autor:** Tutos Rive  
**Soporte:** [support@dev2forge.software](mailto:support@dev2forge.software)
