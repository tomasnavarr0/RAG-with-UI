# Asistente Legal con OpenAI y Chainlit

Este repositorio contiene un asistente virtual diseñado para ayudar en tareas legales, aprovechando los servicios de OpenAI y la plataforma LiteralAI. El asistente está configurado para utilizar APIs de ambas plataformas para el procesamiento y generación de respuestas.

## Estructura del proyecto

- **`scripts/`**: Contiene los scripts principales del proyecto.
  - **`app.py`**: Punto de entrada de la aplicación.
  - **`config.py`**: Archivo de configuración para inicializar clientes de OpenAI y LiteralAI.
  - **`audio.py`**: Maneja la funcionalidad de conversión de texto a voz.
  - **`chat.py`**: Contiene la lógica principal para gestionar las conversaciones.
  - **`event_handler.py`**: Define los eventos específicos que el asistente debe manejar.
  - **`file_utils.py`**: Funciones para la gestión de archivos.
- **`Dockerfile`**: Configuración para construir la imagen Docker del asistente.
- **`venv/`**: Entorno virtual para gestionar las dependencias del proyecto.

## Requisitos previos

- Python 3.8+
- Una cuenta de OpenAI con claves API
- Docker (opcional para la ejecución en un contenedor)

## Configuración

### Variables de Entorno

Antes de ejecutar el proyecto, asegúrate de tener configuradas las siguientes variables de entorno:

- **`OPENAI_API_KEY`**: Clave API de OpenAI.
- **`ASSISTANT_ID`**: ID del asistente de OpenAI.
- **`LITERAL_API_KEY`**: Clave API de LiteralAI.

Puedes agregar estas variables en tu entorno local o en un archivo `.env` para Docker.

### Instalación

1. Clona el repositorio:

```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
```

## Instalación

Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Ejecutar el asistente
```bash
chainlit run app.py -w
```

### APIKEYS
- Generar una api key en openai
- Entrar a literalAI con el mail de vanguard y buscar tu proyecto, entrar a la configuracion y copiar la apikey de literalai
