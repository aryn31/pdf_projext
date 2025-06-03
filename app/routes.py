from fastapi import APIRouter, UploadFile, File, Form
from app.utils import extract_text_from_pdf, chunk_text
from app.embedding import embed_and_store, search_similar_chunks
from app.llm import query_local_llm

router = APIRouter()
docs = []

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    global docs
    text = extract_text_from_pdf(file.file)
    docs = chunk_text(text)
    embed_and_store(docs)
    return {"message": f"Uploaded and indexed {len(docs)} chunks."}

@router.post("/ask")
async def ask(question: str = Form(...)):
    indices = search_similar_chunks(question)
    context = "\n".join([docs[i] for i in indices])
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    answer = query_local_llm(prompt)
    return {"answer": answer.strip()}
