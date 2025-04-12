import os
import csv
import time
from PyPDF2 import PdfReader, PdfWriter

from app.config import Settings


# ID de la base de datos vectorial ya creada
vector_store_id = "vs_67f9c22c5f188191843d60cd1a9bbd24"

# Ruta a la carpeta que contiene los PDFs
pdf_folder = "app/data"

# Nombre del archivo CSV para guardar la información
csv_file = "vector_store_files.csv"

# Crear o cargar el CSV para almacenar el archivo_id, vector_store_id, y otros datos
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["file_name", "file_id", "vector_store_id", "created_at"])


# Función para dividir un PDF en chunks de tamaño máximo
def chunk_pdf(pdf_path, max_chunk_size_mb=5):
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    chunks = []
    current_chunk = PdfWriter()
    max_chunk_size_bytes = max_chunk_size_mb * 1024 * 1024  # Convertir MB a bytes

    for i in range(total_pages):
        current_chunk.add_page(reader.pages[i])

        # Guardar temporalmente el chunk para calcular su tamaño
        temp_chunk_path = f"{pdf_path[:-4]}_temp_chunk.pdf"
        with open(temp_chunk_path, "wb") as temp_pdf:
            current_chunk.write(temp_pdf)

        # Verificar el tamaño del chunk
        current_chunk_size = os.path.getsize(temp_chunk_path)

        if current_chunk_size > max_chunk_size_bytes:
            # Si el tamaño excede el límite, guardar el chunk actual
            chunk_path = f"{pdf_path[:-4]}_chunk_{len(chunks)}.pdf"
            with open(chunk_path, "wb") as output_pdf:
                current_chunk.write(output_pdf)

            chunks.append(chunk_path)

            # Reiniciar el writer y agregar la página actual al nuevo chunk
            current_chunk = PdfWriter()
            current_chunk.add_page(reader.pages[i])

    # Guardar el último chunk si tiene páginas
    if len(current_chunk.pages) > 0:
        chunk_path = f"{pdf_path[:-4]}_chunk_{len(chunks)}.pdf"
        with open(chunk_path, "wb") as output_pdf:
            current_chunk.write(output_pdf)
        chunks.append(chunk_path)

    # Limpiar el archivo temporal
    if os.path.exists(temp_chunk_path):
        os.remove(temp_chunk_path)

    return chunks


# Función para subir archivos PDF a OpenAI
def upload_pdf_to_openai(pdf_path):
    try:
        with open(pdf_path, "rb") as f:
            response = Settings.openai_client.files.create(file=f, purpose="assistants")
            return response.id
    except Exception as e:
        print(f"Error al subir {pdf_path}: {str(e)}")
        return None


# Lista de archivos PDF
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Subir los archivos divididos y obtener sus streams
file_streams = []
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    print(f"Dividiendo archivo: {pdf_file}")

    try:
        chunks = chunk_pdf(pdf_path)
        for chunk in chunks:
            chunk_size = os.path.getsize(chunk)
            print(f"Subiendo chunk: {chunk} (tamaño: {chunk_size / (1024 * 1024):.2f} MB)")
            file_id = upload_pdf_to_openai(chunk)
            if file_id:  # Solo agrega si la subida fue exitosa
                file_streams.append(open(chunk, "rb"))

                # Guardar en el CSV
                with open(csv_file, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([chunk, file_id, vector_store_id, time.time()])

    except Exception as e:
        print(f"Error al dividir el archivo {pdf_file}: {e}")

# Añadir archivos subidos a la vector store existente y hacer polling del estado
if file_streams:
    try:
        file_batch = Settings.openai_client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id, files=file_streams
        )

        print(f"Estado del batch de archivos: {file_batch.status}")
        print(f"Conteo de archivos: {file_batch.file_counts}")

        if file_batch.status == "failed" or file_batch.file_counts.failed > 0:
            print("Los siguientes archivos fallaron:")
            for idx in range(file_batch.file_counts.failed):
                print(f"Archivo {idx + 1}: {file_streams[idx]}")  # Imprimir el nombre del archivo que falló
        else:
            print("Archivos subidos exitosamente.")

    except Exception as e:
        print(f"Error al añadir los archivos a la vector store: {str(e)}")
    finally:
        for file in file_streams:
            file.close()  # Asegúrate de cerrar los archivos después de usarlos
else:
    print("No se subieron archivos, no se puede añadir a la vector store.")
