# Cómo editar el sitio

- **Datos de contacto, WhatsApp, correo, CRM, Google Analytics y Meta Pixel:** solo se editan en `config.js` (raíz).
- **Textos, menú, pie de página y formularios:** viven en `_herramientas/generar_sitio.py`. Después de editar, regenera todas las páginas:

```bash
python3 _herramientas/generar_sitio.py .
```

  Si editas un `index.html` a mano, ese cambio se pierde la próxima vez que se regenere el sitio.
- **Estilos:** `styles.css`. **Comportamiento (menú, formularios, analítica):** `script.js`.
- La carpeta `_herramientas` no se publica: GitHub Pages ignora las carpetas que empiezan con `_`.
