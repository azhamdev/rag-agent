from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session, col, select
from starlette import status

from app.core.settings import settings
from app.models.database import Document, DocumentPage
from app.models.engine import get_session
from app.modules.document.schema import (
    DocumentDetailResponse,
    DocumentPageResponse,
    DocumentResponse,
    DocumentUploadResponse,
)
from app.modules.document.tasks import extract_document

document_router = APIRouter(prefix="/document", tags=["document"])


@document_router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    session: Session = Depends(get_session),
) -> list[DocumentResponse]:
    documents = session.exec(select(Document)).all()
    return [
        DocumentResponse(
            id=document.id, filename=document.filename, status=document.status
        )
        for document in documents
    ]


@document_router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    document_id: int,
    page_number: int | None = None,
    session: Session = Depends(get_session),
) -> DocumentDetailResponse:
    document = session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    statement = select(DocumentPage).where(DocumentPage.document_id == document_id)
    if page_number is not None:
        statement = statement.where(DocumentPage.page_number == page_number)

    pages = session.exec(statement.order_by(col(DocumentPage.page_number))).all()
    if page_number is not None and not pages:
        raise HTTPException(status_code=404, detail="Document Page not found")

    return DocumentDetailResponse(
        id=document_id,
        filename=document.filename,
        status=document.status,
        page=[
            DocumentPageResponse(
                page_number=page.page_number,
                content=page.content,
                keypoints=page.keypoints,
            )
            for page in pages
        ],
    )


@document_router.post(
    "/", response_model=DocumentUploadResponse, status_code=status.HTTP_202_ACCEPTED
)
async def upload_document(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> DocumentUploadResponse:
    filename = Path(file.filename or "document.pdf").name
    content_type = file.content_type or "application/pdf"

    document = Document(
        filename=filename,
        content_type=content_type,
        status="queued",
    )
    session.add(document)
    session.commit()
    session.refresh(document)

    document_id = document.id
    if document_id is None:
        raise RuntimeError("Document ID was not created")

    upload_dir = Path(settings.document_upload_dir) / str(document_id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / filename
    file_path.write_bytes(await file.read())

    task = extract_document.delay(
        document_id,
        str(file_path),
        filename,
        content_type,
    )

    return DocumentUploadResponse(
        document_id=document_id,
        task_id=task.id,
        filename=filename,
        status="queued",
    )
