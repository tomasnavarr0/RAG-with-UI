from dataclasses import dataclass, field
import os
import csv
import time
from PyPDF2 import PdfReader, PdfWriter

from app.config import Settings


@dataclass
class VectorDB:
    pdf_folder: str = field(default=Settings.PDF_FOLDER)
    csv_file: str = field(default=Settings.CSV_FILE)

    @staticmethod
    def upload_pdf_to_openai(pdf_path: str) -> str:
        try:
            with open(pdf_path, "rb") as f:
                response = Settings.openai_client.files.create(file=f, purpose="assistants")
                return response.id
        except Exception as e:
            raise e

    def create_csv(self) -> None:
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["file_name", "file_id", "vector_store_id", "created_at"])

    @property
    def pdf_files(self) -> list[str]:
        return [f for f in os.listdir(self.pdf_folder) if f.endswith(".pdf")]

    @staticmethod
    def chunk_pdf(pdf_path: str, max_chunk_size_mb: int = 5) -> list[str]:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        chunks: list[str] = []
        current_chunk = PdfWriter()
        max_chunk_size_bytes = max_chunk_size_mb * 1024 * 1024
        temp_chunk_path = f"{pdf_path[:-4]}_temp_chunk.pdf"

        for i in range(total_pages):
            current_chunk.add_page(reader.pages[i])
            with open(temp_chunk_path, "wb") as temp_pdf:
                current_chunk.write(temp_pdf)

            current_chunk_size = os.path.getsize(temp_chunk_path)

            if current_chunk_size > max_chunk_size_bytes:
                chunk_path = f"{pdf_path[:-4]}_chunk_{len(chunks)}.pdf"
                chunks.append(chunk_path)
                current_chunk = PdfWriter()
                current_chunk.add_page(reader.pages[i])

        if len(current_chunk.pages) > 0:
            chunk_path: str = f"{pdf_path[:-4]}_chunk_{len(chunks)}.pdf"
            with open(chunk_path, "wb") as output_pdf:
                current_chunk.write(output_pdf)
            chunks.append(chunk_path)

        if os.path.exists(temp_chunk_path):
            os.remove(temp_chunk_path)

        return chunks

    def upload_chunks_to_openai(self) -> None:
        file_streams = []
        for pdf_file in self.pdf_files:
            pdf_path = os.path.join(self.pdf_folder, pdf_file)

            chunks = self.chunk_pdf(pdf_path)

            for chunk in chunks:
                file_id = self.upload_pdf_to_openai(chunk)
                if file_id:
                    file_streams.append(open(chunk, "rb"))

                    with open(self.csv_file, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([chunk, file_id, Settings.VECTOR_DB_ID, time.time()])

        if file_streams:
            try:
                file_batch = Settings.openai_client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=Settings.VECTOR_DB_ID, files=file_streams
                )
            except Exception as e:
                print(f"Error al añadir los archivos a la vector store: {str(e)}")
            finally:
                for file in file_streams:
                    file.close()
        else:
            print("No se subieron archivos, no se puede añadir a la vector store.")
