from pathlib import Path
from chainlit.element import ElementBased
from openai import AsyncOpenAI
from dataclasses import dataclass
from openai.types.beta.threads.message_create_params import Attachment


@dataclass
class FileUtilsWrapper:
    openai_client: AsyncOpenAI

    async def get_file(self, path: str) -> str:
        file_object = await self.openai_client.files.create(file=Path(path), purpose="assistants")
        return file_object.id

    async def _upload_files(self, files: list[ElementBased]) -> list[str]:
        return [await self.get_file(file.path) for file in files if file.path]

    async def process_files(self, files: list[ElementBased]) -> list[Attachment]:
        file_ids = await self._upload_files(files)
        return [
            {
                "file_id": file_id,
                "tools": [{"type": "file_search"}],
            }
            for file_id in file_ids
        ]
