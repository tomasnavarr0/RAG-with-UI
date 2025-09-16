from dataclasses import dataclass, field
import os
from openai import AsyncOpenAI
from app.config import Settings
from app.models import VectorFile


@dataclass
class OpenAIVectorDB:
    openai_client: AsyncOpenAI = field(default=AsyncOpenAI(api_key=Settings.OPENAI_API_KEY))
    pdf_folder: str = field(default=Settings.PDF_FOLDER)

    @property
    def pdf_files(self) -> list[str]:
        return ["app/data/" + file for file in os.listdir(self.pdf_folder) if file.endswith(".pdf")]

    async def upsert(self, file_path: str) -> VectorFile:
        with open(file_path, "rb") as file_obj:
            file = await self.openai_client.files.create(file=file_obj, purpose="assistants")
            await self.openai_client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=Settings.VECTOR_DB_ID, files=[file_obj]
            )
            return VectorFile(id=file.id, filename=file.filename)

    async def upsert_all(self, files_path: list[str] | None = None) -> list[VectorFile]:
        files_uploaded = list[VectorFile]()
        files = files_path or await self.get_all
        all_filenames = ["app/data/" + file.filename for file in files]  # type: ignore[union-attr]
        for file_path in self.pdf_files:
            if file_path in all_filenames:
                continue
            uploaded_file = await self.upsert(file_path)
            files_uploaded.append(uploaded_file)
        return files_uploaded

    @property
    async def get_all(self) -> list[VectorFile]:
        file_list = await self.openai_client.files.list()
        return [VectorFile(id=file.id, filename=file.filename) for file in file_list.data]

    async def delete(self, file_id: str) -> VectorFile:
        file = await self.openai_client.files.delete(file_id)
        return VectorFile(id=file.id, filename="deleted", deleted=True)

    async def delete_all(self) -> list[VectorFile]:
        files = await self.get_all
        return [await self.delete(file.id) for file in files]
