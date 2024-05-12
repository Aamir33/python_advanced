#Building Docker Image
FROM python:3.11-slim
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install transformers
RUN pip install pymupdf
COPY src /src
RUN chmod 777 /src/*
RUN mkdir /logs
WORKDIR /src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive", "300"]
