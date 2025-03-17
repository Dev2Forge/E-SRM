from PIL import Image, ImageEnhance, ImageFilter

def apply_filters(image, brightness, contrast, saturation, gamma, hue, sharpness):
    img = image.copy()
    # Aplicar nitidez
    unsharp_mask = ImageFilter.UnsharpMask(
        radius=2, percent=int((sharpness - 1.0) * 150 + 100), threshold=3
    )
    img = img.filter(unsharp_mask)
    # Brillo
    img = ImageEnhance.Brightness(img).enhance(1.0 + brightness)
    # Contraste
    img = ImageEnhance.Contrast(img).enhance(contrast)
    # Saturación
    img = ImageEnhance.Color(img).enhance(saturation)
    # Gamma
    if gamma != 1.0:
        from math import pow
        lut = [int(255 * pow((i/255), 1/gamma)) for i in range(256)]
        num_channels = len(img.getbands())
        img = img.point(lut * num_channels)
    # Hue
    if hue != 0:
        img = img.convert("HSV")
        hdata = list(img.getdata())
        new_data = []
        for h, s, v in hdata:
            hd = (h * 360.0 / 255.0 + hue) % 360
            new_data.append((int(hd / 360.0 * 255), s, v))
        img.putdata(new_data)
        img = img.convert("RGBA")
    return img

def cover_image(image, container_w, container_h):
    """
    Aplica el efecto "cover" similar a CSS:
    Escala la imagen manteniendo su aspecto y recorta lo que sobre para llenar 
    el contenedor (de dimensiones fijas) sin dejar espacios.
    """
    img_w, img_h = image.size
    img_ratio = img_w / img_h
    container_ratio = container_w / container_h
    if img_ratio > container_ratio:
        # La imagen es más ancha: igualamos altura y recortamos laterales
        new_height = container_h
        new_width = int(new_height * img_ratio)
        img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        left = (new_width - container_w) // 2
        img = img.crop((left, 0, left + container_w, container_h))
    else:
        # La imagen es más alta: igualamos ancho y recortamos arriba/abajo
        new_width = container_w
        new_height = int(new_width / img_ratio)
        img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        top = (new_height - container_h) // 2
        img = img.crop((0, top, container_w, top + container_h))
    return img
