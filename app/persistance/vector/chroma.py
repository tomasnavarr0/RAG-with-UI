from dataclasses import dataclass, field
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from app.config import Settings
from app.models import VectorFile
from .abstract import AbstractVectorDB


@dataclass
class ChromaVectorDB(AbstractVectorDB):
    embedding_function: HuggingFaceEmbeddings = field(
        default_factory=lambda: HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    persist_directory: str = field(default=Settings.CHROMA_PERSIST_DIRECTORY)
    text_splitter: RecursiveCharacterTextSplitter = field(
        default_factory=lambda: RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    )

    @property
    def chroma_client(self) -> Chroma:
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function,
        )

    @property
    def pdf_files(self) -> list[str]:
        return [
            os.path.join(Settings.PDF_FOLDER, file) for file in os.listdir(Settings.PDF_FOLDER) if file.endswith(".pdf")
        ]

    async def upsert(self, file_path: str) -> VectorFile:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)

        file_id = os.path.basename(file_path)
        ids = [f"{file_id}-{i}" for i in range(len(chunks))]

        self.chroma_client.add_documents(chunks, ids=ids)
        self.chroma_client.persist()

        return VectorFile(id=file_id, filename=file_id)

    async def upsert_all(self, files_path: list[str] | None = None) -> list[VectorFile]:
        files = files_path or self.pdf_files
        return [await self.upsert(file_path) for file_path in files]

    async def get_all(self) -> list[VectorFile]:
        return [VectorFile(id=os.path.basename(f), filename=os.path.basename(f)) for f in self.pdf_files]

    async def delete(self, file_id: str) -> VectorFile:
        self.chroma_client.delete(where={"id": {"$regex": f"^{file_id}"}})
        self.chroma_client.persist()
        return VectorFile(id=file_id, filename="deleted", deleted=True)

    async def delete_all(self) -> list[VectorFile]:
        files = await self.get_all()
        return [await self.delete(file.id) for file in files]
