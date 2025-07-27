# Vic3-reader
Análisis en tiempo real de los nuevos posts que se generan en bluesky

### ¿Qué es?

Es una aplicación que se encarga de leer saves de Victoria 3 y convertirlo a un diccionario anidado. El diccionario se puede explorar para sacar cada valor del archivo save según la semántica definida por Paradox. 

Como objetivo final, vamos a tener una mini-ETL que sea capaz de:
1. Encontrar en la carpeta 'saves' archivos de .v3 (en texto plano).
2. Obtener métricas para unos países (TAGs) definidos.
3. Guardar el resultado en un excel para.

##### módulo parser
Define la gramática para poder estructurar los saves y cargarlos correctamente en Python.

##### módulos utils
Define (a) cómo encontrar y leer los saves. Opcional, también define cómo guardar el archiv en JSON para no repetir el uso del parser cada vez.

Define (b) la lógica para crear una interfaz que te permite explorar interactivamente los datos del save.

##### módulo metrics
Define la semántica para explorar y obtener los datos del juego una vez convertido a un diccionario anidado.

## TODO List
Ver markdown TODO.md

## Entorno de desarrollo

Para el desarrollo de esta aplicación, se usa la herramienta [uv](https://docs.astral.sh/uv/), que es una herramienta de gestión de paquetes y dependencias para Python. Ver la página de instalación [aquí](https://docs.astral.sh/uv/getting-started/installation/).

### Uso de uv

Para instalar las dependencias, se puede usar el comando:

```bash
uv sync
```

Para añadir una dependencia, se puede usar el comando:

```bash
uv add <nombre_de_la_dependencia>
```

Esto es similar a usar `pip install <nombre_de_la_dependencia>`. Las dependencias se encuentran en el archivo `pyproject.toml` y en el archivo `uv.lock` (que no hay que añadir al `.gitignore`).

Para ejecutar el script, se puede usar el comando:

```bash
uv run <nombre_del_script>
```

## Git

Para escribir los mensajes de los commits, vamos a usar el formato de [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).