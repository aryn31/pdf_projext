from fastapi import APIRouter, UploadFile, File, Form
from app.utils import extract_text_from_pdf, chunk_text, extract_images_from_pdf
from app.embedding import embed_and_store, search_similar_chunks
from app.llm import query_local_llm
from app.llava import query_llava

router = APIRouter()
docs = []
image_captions = []

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    global docs, image_captions
    text = extract_text_from_pdf(file.file)
    docs = chunk_text(text)
    embed_and_store(docs)

    # Extract image captions
    file.file.seek(0)
    images = extract_images_from_pdf(file.file)
    image_captions = [query_llava(img) for img in images]

    return {"message": f"Uploaded and indexed {len(docs)} chunks and {len(image_captions)} image captions."}

@router.post("/ask")
async def ask(question: str = Form(...)):
    indices = search_similar_chunks(question)
    context = "\n".join([docs[i] for i in indices])
    image_context = "\n".join(image_captions)
    full_prompt = f"""
You are a helpful assistant.

Use both the text context and image descriptions to answer the question.

TEXT CONTEXT:
{context}

IMAGE CONTEXT:
{image_context}

QUESTION:
{question}

ANSWER:"""
    answer = query_local_llm(full_prompt)
    return {"answer": answer.strip()}
