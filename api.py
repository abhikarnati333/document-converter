#!/usr/bin/env python3
"""
Document Converter API - REST API for converting HTML/Markdown to PDF
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from pathlib import Path
import uuid
from typing import Optional
import markdown2
from weasyprint import HTML, CSS
from PIL import Image
import io
import zipfile
import shutil

app = FastAPI(
    title="Document Converter API",
    description="Convert HTML and Markdown files to PDFs and Images",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for temporary files
TEMP_DIR = tempfile.gettempdir()
CSS_PATH = os.path.join(os.path.dirname(__file__), 'style.css')


def markdown_to_html(markdown_content: str) -> str:
    """Convert Markdown content to HTML."""
    html = markdown2.markdown(
        markdown_content,
        extras=[
            'fenced-code-blocks',
            'tables',
            'break-on-newline',
            'header-ids',
            'code-friendly',
            'footnotes',
            'strike',
            'task_list'
        ]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {html}
</body>
</html>"""


def html_to_pdf(html_content: str, output_path: str, custom_css: Optional[str] = None) -> bool:
    """Convert HTML content to PDF with Google Docs styling."""
    try:
        # Ensure complete HTML document
        if '<html' not in html_content.lower():
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {html_content}
</body>
</html>"""
        
        # Prepare stylesheets
        stylesheets = []
        if custom_css:
            # Save custom CSS to temp file
            temp_css = os.path.join(TEMP_DIR, f"custom_{uuid.uuid4().hex}.css")
            with open(temp_css, 'w', encoding='utf-8') as f:
                f.write(custom_css)
            stylesheets.append(CSS(filename=temp_css))
        elif os.path.exists(CSS_PATH):
            stylesheets.append(CSS(filename=CSS_PATH))
        
        # Generate PDF
        html_obj = HTML(string=html_content)
        html_obj.write_pdf(output_path, stylesheets=stylesheets)
        
        # Clean up temp CSS if created
        if custom_css:
            try:
                os.remove(temp_css)
            except:
                pass
        
        return True
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        return False


def html_to_image(html_content: str, output_path: str, image_format: str = 'png', 
                  custom_css: Optional[str] = None, width: int = 1200) -> str:
    """Convert HTML content to Image (PNG, JPG, etc.). Returns path to output file (could be .zip for multi-page)."""
    try:
        # Ensure complete HTML document
        if '<html' not in html_content.lower():
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {html_content}
</body>
</html>"""
        
        # Prepare stylesheets
        stylesheets = []
        if custom_css:
            # Save custom CSS to temp file
            temp_css = os.path.join(TEMP_DIR, f"custom_{uuid.uuid4().hex}.css")
            with open(temp_css, 'w', encoding='utf-8') as f:
                f.write(custom_css)
            stylesheets.append(CSS(filename=temp_css))
        elif os.path.exists(CSS_PATH):
            stylesheets.append(CSS(filename=CSS_PATH))
        
        # Generate PDF first (WeasyPrint can't directly export to image)
        temp_pdf = os.path.join(TEMP_DIR, f"temp_{uuid.uuid4().hex}.pdf")
        html_obj = HTML(string=html_content)
        html_obj.write_pdf(temp_pdf, stylesheets=stylesheets)
        
        # Convert PDF to image using pdf2image
        try:
            from pdf2image import convert_from_path
            
            # Convert ALL pages to images
            images = convert_from_path(temp_pdf, dpi=150)
            
            if not images:
                print("No images generated from PDF")
                return None
            
            print(f"DEBUG: Generated {len(images)} page(s)")
            
            # If multiple pages, create a zip file with individual images
            if len(images) > 1:
                print(f"DEBUG: Creating ZIP file for {len(images)} pages")
                # Create a temporary directory for images
                temp_image_dir = os.path.join(TEMP_DIR, f"pages_{uuid.uuid4().hex}")
                os.makedirs(temp_image_dir, exist_ok=True)
                
                try:
                    # Save each page as a separate image
                    for idx, img in enumerate(images, start=1):
                        page_filename = f"page_{idx:03d}.{image_format.lower()}"
                        page_path = os.path.join(temp_image_dir, page_filename)
                        
                        # Convert RGBA to RGB for JPEG if needed
                        if image_format.lower() in ['jpg', 'jpeg'] and img.mode == 'RGBA':
                            rgb_img = Image.new('RGB', img.size, 'white')
                            rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
                            img = rgb_img
                        
                        # Save the image
                        if image_format.lower() in ['jpg', 'jpeg']:
                            img.save(page_path, 'JPEG', quality=95)
                        else:
                            img.save(page_path, 'PNG')
                    
                    # Create a zip file containing all images
                    zip_output_path = output_path.replace(f'.{image_format.lower()}', '.zip')
                    with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for filename in sorted(os.listdir(temp_image_dir)):
                            file_path = os.path.join(temp_image_dir, filename)
                            zipf.write(file_path, filename)
                    
                    # Return path to zip file
                    return zip_output_path
                    
                finally:
                    # Clean up temporary image directory
                    try:
                        shutil.rmtree(temp_image_dir)
                    except:
                        pass
            else:
                # Single page - save directly
                if image_format.lower() in ['jpg', 'jpeg']:
                    # Convert RGBA to RGB for JPEG
                    img = images[0]
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    img.save(output_path, 'JPEG', quality=95)
                else:
                    images[0].save(output_path, 'PNG')
            
            # Return the path to the output file
            return output_path
                    
        except ImportError:
            # Fallback: just return error
            print("pdf2image not installed. Install with: pip install pdf2image")
            return None
        finally:
            # Clean up temp files
            try:
                os.remove(temp_pdf)
                if custom_css:
                    os.remove(temp_css)
            except:
                pass
        
    except Exception as e:
        print(f"Error converting to image: {e}")
        return None


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "Document Converter API",
        "version": "2.0.0",
        "endpoints": {
            "POST /convert/markdown": "Convert Markdown content to PDF",
            "POST /convert/html": "Convert HTML content to PDF",
            "POST /convert/file": "Upload and convert a file to PDF",
            "POST /convert/markdown/image": "Convert Markdown content to Image",
            "POST /convert/html/image": "Convert HTML content to Image",
            "POST /convert/file/image": "Upload and convert a file to Image",
            "GET /health": "Health check endpoint"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/convert/markdown")
async def convert_markdown(
    content: str = Form(...),
    filename: Optional[str] = Form("document.pdf"),
    custom_css: Optional[str] = Form(None)
):
    """
    Convert Markdown content to PDF.
    
    - **content**: Markdown content as string
    - **filename**: Optional output filename (default: document.pdf)
    - **custom_css**: Optional custom CSS styling
    """
    try:
        # Generate unique filename
        pdf_filename = filename if filename.endswith('.pdf') else f"{filename}.pdf"
        pdf_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_{pdf_filename}")
        
        # Convert Markdown to HTML
        html_content = markdown_to_html(content)
        
        # Convert to PDF
        success = html_to_pdf(html_content, pdf_path, custom_css)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=pdf_filename,
            background=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting Markdown: {str(e)}")


@app.post("/convert/html")
async def convert_html(
    content: str = Form(...),
    filename: Optional[str] = Form("document.pdf"),
    custom_css: Optional[str] = Form(None)
):
    """
    Convert HTML content to PDF.
    
    - **content**: HTML content as string
    - **filename**: Optional output filename (default: document.pdf)
    - **custom_css**: Optional custom CSS styling
    """
    try:
        # Generate unique filename
        pdf_filename = filename if filename.endswith('.pdf') else f"{filename}.pdf"
        pdf_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_{pdf_filename}")
        
        # Convert to PDF
        success = html_to_pdf(content, pdf_path, custom_css)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=pdf_filename,
            background=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting HTML: {str(e)}")


@app.post("/convert/file")
async def convert_file(
    file: UploadFile = File(...),
    custom_css: Optional[str] = Form(None)
):
    """
    Upload and convert a file (Markdown or HTML) to PDF.
    
    - **file**: File upload (.md, .markdown, .html, .htm)
    - **custom_css**: Optional custom CSS styling
    """
    try:
        # Validate file type
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.md', '.markdown', '.html', '.htm']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported: .md, .markdown, .html, .htm"
            )
        
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Generate output filename
        output_filename = Path(file.filename).stem + '.pdf'
        pdf_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_{output_filename}")
        
        # Convert based on file type
        if file_ext in ['.md', '.markdown']:
            html_content = markdown_to_html(content_str)
        else:
            html_content = content_str
        
        # Convert to PDF
        success = html_to_pdf(html_content, pdf_path, custom_css)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=output_filename,
            background=None
        )
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting file: {str(e)}")


# ============================================================================
# IMAGE CONVERSION ENDPOINTS
# ============================================================================

@app.post("/convert/markdown/image")
async def convert_markdown_to_image(
    content: str = Form(...),
    filename: Optional[str] = Form("document.png"),
    image_format: Optional[str] = Form("png"),
    custom_css: Optional[str] = Form(None),
    width: Optional[int] = Form(1200)
):
    """
    Convert Markdown content to Image (PNG, JPG, JPEG).
    
    - **content**: Markdown content as string
    - **filename**: Optional output filename (default: document.png)
    - **image_format**: Image format - png, jpg, or jpeg (default: png)
    - **custom_css**: Optional custom CSS styling
    - **width**: Image width in pixels (default: 1200)
    """
    try:
        # Validate image format
        image_format = image_format.lower()
        if image_format not in ['png', 'jpg', 'jpeg']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image format: {image_format}. Supported: png, jpg, jpeg"
            )
        
        # Generate unique filename
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            filename = f"{filename}.{image_format}"
        
        image_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_{filename}")
        
        # Convert Markdown to HTML
        html_content = markdown_to_html(content)
        
        # Convert to Image
        result_path = html_to_image(html_content, image_path, image_format, custom_css, width)
        
        if not result_path:
            raise HTTPException(status_code=500, detail="Failed to generate image")
        
        # Check if result is a zip file (multi-page)
        if result_path.endswith('.zip'):
            media_type = "application/zip"
            filename = filename.replace(f'.{image_format}', '.zip')
            return FileResponse(
                result_path,
                media_type=media_type,
                filename=filename,
                background=None
            )
        else:
            # Single page - return image
            media_type = "image/png" if image_format == "png" else "image/jpeg"
            return FileResponse(
                result_path,
                media_type=media_type,
                filename=filename,
                background=None
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting Markdown to image: {str(e)}")


@app.post("/convert/html/image")
async def convert_html_to_image(
    content: str = Form(...),
    filename: Optional[str] = Form("document.png"),
    image_format: Optional[str] = Form("png"),
    custom_css: Optional[str] = Form(None),
    width: Optional[int] = Form(1200)
):
    """
    Convert HTML content to Image (PNG, JPG, JPEG).
    
    - **content**: HTML content as string
    - **filename**: Optional output filename (default: document.png)
    - **image_format**: Image format - png, jpg, or jpeg (default: png)
    - **custom_css**: Optional custom CSS styling
    - **width**: Image width in pixels (default: 1200)
    """
    try:
        # Validate image format
        image_format = image_format.lower()
        if image_format not in ['png', 'jpg', 'jpeg']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image format: {image_format}. Supported: png, jpg, jpeg"
            )
        
        # Generate unique filename
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            filename = f"{filename}.{image_format}"
        
        image_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_{filename}")
        
        # Convert to Image
        result_path = html_to_image(content, image_path, image_format, custom_css, width)
        
        if not result_path:
            raise HTTPException(status_code=500, detail="Failed to generate image")
        
        # Check if result is a zip file (multi-page)
        if result_path.endswith('.zip'):
            media_type = "application/zip"
            filename = filename.replace(f'.{image_format}', '.zip')
            return FileResponse(
                result_path,
                media_type=media_type,
                filename=filename,
                background=None
            )
        else:
            # Single page - return image
            media_type = "image/png" if image_format == "png" else "image/jpeg"
            return FileResponse(
                result_path,
                media_type=media_type,
                filename=filename,
                background=None
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting HTML to image: {str(e)}")


@app.post("/convert/file/image")
async def convert_file_to_image(
    file: UploadFile = File(...),
    image_format: Optional[str] = Form("png"),
    custom_css: Optional[str] = Form(None),
    width: Optional[int] = Form(1200)
):
    """
    Upload and convert a file (Markdown or HTML) to Image (PNG, JPG, JPEG).
    
    - **file**: File upload (.md, .markdown, .html, .htm)
    - **image_format**: Image format - png, jpg, or jpeg (default: png)
    - **custom_css**: Optional custom CSS styling
    - **width**: Image width in pixels (default: 1200)
    """
    try:
        # Validate file type
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.md', '.markdown', '.html', '.htm']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported: .md, .markdown, .html, .htm"
            )
        
        # Validate image format
        image_format = image_format.lower()
        if image_format not in ['png', 'jpg', 'jpeg']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image format: {image_format}. Supported: png, jpg, jpeg"
            )
        
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Generate output filename
        output_filename = Path(file.filename).stem + f'.{image_format}'
        image_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_{output_filename}")
        
        # Convert based on file type
        if file_ext in ['.md', '.markdown']:
            html_content = markdown_to_html(content_str)
        else:
            html_content = content_str
        
        # Convert to Image
        result_path = html_to_image(html_content, image_path, image_format, custom_css, width)
        
        if not result_path:
            raise HTTPException(status_code=500, detail="Failed to generate image")
        
        # Check if result is a zip file (multi-page)
        if result_path.endswith('.zip'):
            media_type = "application/zip"
            output_filename = output_filename.replace(f'.{image_format}', '.zip')
            return FileResponse(
                result_path,
                media_type=media_type,
                filename=output_filename,
                background=None
            )
        else:
            # Single page - return image
            media_type = "image/png" if image_format == "png" else "image/jpeg"
            return FileResponse(
                result_path,
                media_type=media_type,
                filename=output_filename,
                background=None
            )
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting file to image: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
