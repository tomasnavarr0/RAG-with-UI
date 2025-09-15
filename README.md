# Asistente Batty con OpenAI y Chainlit

Este repositorio contiene un asistente virtual diseñado para ayudar en tareas comunes al sistema de Batuta desarrollado por Metabase Q, aprovechando los servicios de OpenAI y la plataforma LiteralAI. El asistente está configurado para utilizar APIs de ambas plataformas para el procesamiento y generación de respuestas.

Las tecnologias usadas son:
- OpenAI para utilizar el LLM y la Bases de Datos vectorial
- Chainlit para creacion del frontend
- LiteralAI para mockear funcionalidades de OpenAI que no son compatibles con Chainlit
- Docker

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
- **`VECTOR_DB_ID`**: Clave API de BD Vectorial.
Puedes agregar estas variables en tu entorno local o en un archivo `.env`.

### Instalación

1. Clona el repositorio:

```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
```

## Instalación

Instala las dependencias:
```bash
docker build -t chainlit-app .
```

### Ejecutar el asistente
```bash
docker run -p 8000:8000 chainlit-app
```

### Mejoras
Integracion a sistemas reales ( APIs ) Esto permitira desbloquear muchas funcionalidades y mejorar la precision de respuesta
