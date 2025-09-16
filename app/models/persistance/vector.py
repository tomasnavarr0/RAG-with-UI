from pydantic import BaseModel, Field, ConfigDict


class VectorFile(BaseModel):
    id_: str = Field(alias="id")
    filename: str
    deleted: bool = False

    model_config = ConfigDict(
        populate_by_name=False,
    )
