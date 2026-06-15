from typing import Any
import base64
from pathlib import Path

from app.core.settings import settings
from app.utils.chromadb import get_chromadb_collection
from app.utils.mistral import get_mistral_client
from app.utils.openai import get_openai_client


def extract_document_with_mistral(
    file_path: str,
    content_type: str,
)-> Any:
    path = Path(file_path)
    base64_document = base64.b64encode(path.read_bytes()).decode("utf-8")

    mistral_client = get_mistral_client()
    return mistral_client.ocr.process(
        model = settings.mistral_ocr_model,
        document={
            "type": "document_url",
            "document_url": f"data:{content_type};base64,{base64_document}"
        },
        include_image_base64=True
    )


def extract_keypoints(content: str) -> str:
    openai_client = get_openai_client()
    response = openai_client.chat.completions.create(
        model = settings.openai_keypoint_model,
        messages=[
            {
                "role":"system",
                "content": (
                    "Extract concise key points as bullets points. Return only bulltets."
                ),
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )

    return response.choices[0].message.content or ""


def insert_page_to_chromadb(
    document_id: int,
    filename: str,
    page_number: int,
    content: str,
    keypoints: str,
) -> None:
    collection = get_chromadb_collection()
    collection.add(
        ids=[f"document-{document_id}-page-{page_number}"],
        documents=[content],
        metadatas=[{
            "document_id": document_id,
            "document_name": filename,
            "page_number": page_number,
            "keypoints": keypoints
        }]
    )
