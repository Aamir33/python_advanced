from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pdftextbookprocessor import PDFTextbookProcessor

app = FastAPI(
    title="REST API Service for Operational Dashboard",
    openapi_url="/dashboard-service/openapi.json", 
    docs_url = "/dashboard-service/docs", 
    redoc_url="/dashboard-service/redoc",
    version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

processor = None

@app.get("/getthellm")
async def initialize_processor(pdf_path: str, selected_chapters: list):
    global processor
    processor = PDFTextbookProcessor(pdf_path, selected_chapters)
    return {"message": "getthellm successfully created"}

@app.post("/question")
async def ask_question(question: str):
    if processor is None:
        return {"error": "Please call /getthellm first."}
    answer = processor.answer_question(question)
    return {"answer": answer}
