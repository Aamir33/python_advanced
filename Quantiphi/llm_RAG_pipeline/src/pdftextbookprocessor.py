import fitz
from fastapi import FastAPI
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration
from transformers import pipeline

class PDFTextbookProcessor:
    def __init__(self, pdf_path, selected_chapters):
        self.pdf_path = pdf_path
        self.selected_chapters = selected_chapters
        self.index = None
        pdf_path = "pdf/ConceptsofBiology-WEB.pdf"
        self.text = self.extract_text_from_pdf(pdf_path)

    def extract_text_from_pdf(self, pdf_path):
        with fitz.open(pdf_path) as pdf_document:
            text = ""
            print(pdf_document.page_count)
            print(pdf_document)
            for page_number in range(5,54):
                page = pdf_document.load_page(page_number)
                text += page.get_text()
        return text

    def create_index(self):
        paragraphs = self.text.split("\n")
        self.index = {}
        start = 0
        for i, para in enumerate(paragraphs):
            end = start + len(para)
            self.index[f"Paragraph {i+1}"] = [start, end]
            start = end + 1

    def answer_question(self, question):
        if not self.index:
            self.create_index()
        tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-base")
        retriever = RagRetriever.from_pretrained("facebook/rag-token-base", index=self.index)
        model = RagTokenForGeneration.from_pretrained("facebook/rag-token-base")
        rag_pipeline = pipeline("rag", model=model, retriever=retriever, tokenizer=tokenizer)
        answer = rag_pipeline(question)
        return answer
