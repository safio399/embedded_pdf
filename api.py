from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from typing import List

import zipfile
import io

app = FastAPI(
    title="PDF Manipulation API",
    description="API for embedding and extracting PDFs",
    version="1.0.0"
)

@app.post("/create_embedded_pdf/", 
    summary="Embed multiple PDFs into one PDF",
    response_description="PDF containing all embedded PDFs")
async def create_embedded_pdf(
    base_pdf: UploadFile = File(..., description="The base PDF file"),
    pdfs_to_embed: List[UploadFile] = File(..., description="List of PDFs to embed")
):
    
    base_pdf_content = await base_pdf.read()
    base_pdf_reader = PdfReader(io.BytesIO(base_pdf_content))
    
    
    pdf_writer = PdfWriter()
    
    
    for page in base_pdf_reader.pages:
        pdf_writer.add_page(page)
    
    
    for pdf in pdfs_to_embed:
        pdf_content = await pdf.read()
        pdf_writer.add_attachment(pdf.filename, pdf_content)
    
    
    output_buffer = BytesIO()
    pdf_writer.write(output_buffer)
    output_buffer.seek(0)
    
    return StreamingResponse(
        output_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment;filename=embedded_pdf.pdf"}
    )

@app.post("/extract_embedded_pdf/",
    summary="Extract all embedded PDFs from a PDF",
    response_description="List of embedded PDFs")
async def extract_embedded_pdf(
    pdf_file: UploadFile = File(..., description="PDF file to extract attachments from")
):
    
    pdf_content = await pdf_file.read()
    pdf_reader = PdfReader(io.BytesIO(pdf_content))
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for name, file_data in pdf_reader.attachments.items():
            
            if isinstance(file_data, list):
                file_data = file_data[0]
            
            if hasattr(file_data, "get_data"):
                file_data = file_data.get_data()
            zip_file.writestr(name, file_data)

    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={
            "Content-Disposition": "attachment; filename=extracted_pdfs.zip"
        })

