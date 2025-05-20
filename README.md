#  PDF Embedder API

A FastAPI web service that embeds multiple PDFs into a single base PDF file (as attachments). Built entirely using binary operations with Swagger support.

---

##  Features

- Upload a base PDF and embed multiple PDFs inside it.
- Fully in-memory (no file saving on disk).
- Automatic interactive Swagger UI.
- Ready to containerize with Docker.

---

##  API Endpoints

### `POST /create_embedded_pdf/`

Embed multiple PDFs into one base PDF.

#### Form Fields:
- `base_pdf`: Base PDF to embed into (file)
- `pdfs_to_embed`: List of PDFs to embed (multiple files)

#### Response:
Returns a downloadable PDF with all embedded PDFs as attachments.

---
### `POST /extract_embedded_pdf/`
Extract embedded PDFs from a PDF.

#### Form Fields:
- `pdf_file`: PDF file containing embedded PDFs (file)
  
#### Response:
Returns a .zip file containing only the embedded (attached) PDF files. The base PDF itself is not included in the ZIP.

---

##  How to Run

###  Local (without Docker)

```bash
pip install fastapi uvicorn pypdf
uvicorn mapi:app --reload
http://localhost:5000/api/docs

