from dataclasses import dataclass, field
import os
from openai import AsyncOpenAI
from openai.pagination import AsyncPage
from openai.types import FileObject
from app.config import Settings


@dataclass
class OpenAIVectorDB:
    openai_client: AsyncOpenAI = field(default=AsyncOpenAI(api_key=Settings.OPENAI_API_KEY))
    pdf_folder: str = field(default=Settings.PDF_FOLDER)

    @property
    def pdf_files(self) -> list[str]:
        return ["app/data/" + file for file in os.listdir(self.pdf_folder) if file.endswith(".pdf")]

    async def add_all(self) -> str:
        files = await self.get_all
        all_filenames = ["app/data/" + file.filename for file in files.data]  # mypy: ignore
        for file_path in self.pdf_files:
            if file_path in all_filenames:
                pass
            with open(file_path, "rb") as file_obj:
                await self.openai_client.files.create(file=file_obj, purpose="assistants")
                await self.openai_client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=Settings.VECTOR_DB_ID, files=[file_obj]
                )
        return "All files uploaded"

    @property
    async def get_all(self) -> AsyncPage[FileObject]:
        return await self.openai_client.files.list()

    async def delete(self, file_id: str) -> str:
        await self.openai_client.files.delete(file_id)
        return "PDF from Vector DB deleted"

    async def delete_all(self) -> str:
        files = await self.get_all
        for file in files.data:
            await self.delete(file.id)

        return "All files deleted"
