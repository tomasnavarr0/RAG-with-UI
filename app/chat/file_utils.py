from pathlib import Path
from app.config import Settings
from chainlit.element import Element
from openai import OpenAI




async def get_file(path: str, openai_client: OpenAI = Settings.OPENAI_API_KEY) -> str:
    file_object = await openai_client.files.create(file=Path(path), purpose="assistants")
    return file_object.id


async def upload_files(files: list[Element]) -> list[str]:
    return [await get_file(file.path) for file in files]


async def process_files(files: list[Element]):
    file_ids = await upload_files(files)
    return [
        {
            "file_id": file_id,
            "tools": [{"type": "file_search"}],
        }
        for file_id in file_ids
    ]
