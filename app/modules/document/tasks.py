# for extracting document

from sqlmodel import Session

from app.models.database import Document, DocumentPage
from app.models.engine import engine
from app.modules.document.methods import (
    extract_document_with_mistral,
    extract_keypoints,
    insert_page_to_chromadb
)
from app.worker import celery_app

@celery_app.task(name="app.modules.document.tasks.extract_document")
def extract_document(
    document_id: int,
    file_path: str,
    filename: str,
    content_type: str,
) -> dict[str, object]:
    ocr_result = extract_document_with_mistral(file_path, content_type)

    with Session(engine) as session:
        document = session.get(Document, document_id)
        if document is None:
            raise RuntimeError("Document not found")

        document.status = "processing"
        session.add(document)

        pages = []
        for page in ocr_result.pages:
            keypoints = extract_keypoints(page.markdown)
            document_page = DocumentPage(
                document_id=document_id,
                page_number=page.index,
                content=page.markdown,
                keypoints=keypoints,
            )
            session.add(document_page)
            pages.append(document_page)
            insert_page_to_chromadb(document_id, filename, page.index, page.markdown, keypoints)

        document.status = "completed"
        session.add(document)
        session.commit()

    return {
        "document_id": document_id,
        "filename": filename,
        "page_count": len(pages),
    }
