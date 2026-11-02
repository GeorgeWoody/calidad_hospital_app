# Calidad App - Hospital Mario Sánchez

## Uso

La aplicación se ejecuta con Streamlit y no requiere Internet mientras se usa:

```bash
pip install pandas streamlit openpyxl
streamlit run main.py
```

Después se carga el libro Excel, se selecciona una hoja y se aplican filtros
combinables por unidad, año, trimestre y estamento. Una selección vacía
significa “todos”.

## Reglas implementadas

- Se homologan variantes sencillas de nombres de unidades y estamentos.
- Una respuesta `No` normalmente produce `No Cumple`.
- En la hoja `Sellado`, la pregunta que contiene `usa barba` es especial:
  `No` produce `Cumple` y cualquier otra respuesta produce `No Cumple`.

Las funciones nuevas tienen comentarios y docstrings en `main.py` y
`normalization.py`.

## Ejecutable para Windows

Se recomienda validar primero con Python. Como Streamlit abre un navegador
local, el ejecutable debe iniciar el servidor y abrir la URL local. El
empaquetado con PyInstaller puede hacerse después de validar la aplicación;
conviene generarlo en Windows para asegurar compatibilidad con Windows 11.
