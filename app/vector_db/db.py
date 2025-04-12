from dataclasses import dataclass, field
import os
from openai import OpenAI
from openai.types import FileObject
from app.config import Settings


@dataclass
class VectorDB:
    openai_client: OpenAI = field(default=Settings.openai_client)
    pdf_folder: str = field(default=Settings.PDF_FOLDER)

    @property
    def pdf_files(self) -> list[str]:
        return ["app/data/" + file for file in os.listdir(self.pdf_folder) if file.endswith(".pdf")]

    def add_all(self) -> str:
        all_filenames = ["app/data/" + file.filename for file in self.get_all]
        for file_path in self.pdf_files:
            if file_path in all_filenames:
                pass
            with open(file_path, "rb") as file_obj:
                self.openai_client.files.create(file=file_obj, purpose="assistants")
                self.openai_client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=Settings.VECTOR_DB_ID, files=[file_obj]
                )
        return "All files uploaded"

    @property
    def get_all(self) -> list[FileObject]:
        return self.openai_client.files.list()

    def delete(self, file_id: str) -> str:
        self.openai_client.files.delete(file_id)
        return "PDF from Vector DB deleted"

    def delete_all(self) -> str:
        for file in self.get_all:
            self.delete(file.id)

        return "All files deleted"
