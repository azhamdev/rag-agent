from sqlmodel import Field, Relationship, SQLModel


class Document(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str
    content_type: str
    status: str = "processing"

    pages: list["DocumentPage"] = Relationship(back_populates="document")


class DocumentPage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    document_id: int = Field(foreign_key="document.id")
    page_number: int
    content: str
    keypoints: str = ""

    document: Document | None = Relationship(back_populates="pages")
