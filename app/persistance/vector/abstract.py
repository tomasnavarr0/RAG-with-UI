from abc import ABC, abstractmethod

from app.models import VectorFile


class AbstractVectorDB(ABC):
    @abstractmethod
    async def upsert(self, file_path: str) -> VectorFile:
        pass

    @abstractmethod
    async def upsert_all(self, files_path: list[str] | None = None) -> list[VectorFile]:
        pass

    @abstractmethod
    @property
    async def get_all(self) -> list[VectorFile]:
        pass

    @abstractmethod
    async def delete(self, file_id: str) -> VectorFile:
        pass

    @abstractmethod
    async def delete_all(self) -> list[VectorFile]:
        pass
