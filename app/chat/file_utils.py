from typing import List
from pathlib import Path
from app.config import Settings
import chainlit as cl
from chainlit.element import Element


async def upload_files(files: List[Element]):
    file_ids = []
    for file in files:
        uploaded_file = await Settings.sync_openai_client.files.create(file=Path(file.path), purpose="assistants")
        file_ids.append(uploaded_file.id)
    return file_ids


async def process_files(files: List[Element]):
    # Upload files if any and get file_ids
    file_ids = []
    if len(files) > 0:
        file_ids = await upload_files(files)

    return [
        {
            "file_id": file_id,
            "tools": [{"type": "file_search"}],
        }
        for file_id in file_ids
    ]
