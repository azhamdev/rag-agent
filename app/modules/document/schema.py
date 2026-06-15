from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int | None
    filename: str
    status: str

class DocumentUploadResponse(BaseModel):
    document_id: int
    task_id: str
    filename: str
    status: str

class DocumentPageResponse(BaseModel):
    page_number: int
    content: str
    keypoints: str

class DocumentDetailResponse(BaseModel):
    id: int
    filename: str
    status: str
    page: list[DocumentPageResponse]

