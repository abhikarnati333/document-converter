# Document Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](Dockerfile)

🚀 A powerful REST API for converting HTML and Markdown to beautifully formatted PDFs and Images.

[Features](#features) • [Quick Start](#quick-start) • [API Documentation](#api-endpoints) • [Docker](#docker-setup-recommended) • [Contributing](CONTRIBUTING.md)

---

## Features

- ✨ REST API for converting Markdown and HTML to **PDF** and **Images** (PNG, JPG)
- 📄 Google Docs-like styling with proper padding and margins
- 🎨 Professional typography and spacing
- 📑 Automatic page breaks and pagination (PDF)
- 🖼️ High-quality image generation with customizable dimensions
- � **Multi-page support**: All pages automatically combined into single tall image
- �🔤 Support for tables, code blocks, lists, and more
- 🌐 CORS enabled for web applications
- 📝 Interactive API documentation (Swagger UI)
- 🚀 Fast and reliable conversion
- 🎯 Also includes command-line interface

## Quick Start

### Using Docker (Recommended)

```bash
git clone https://github.com/YOUR_USERNAME/document-converter.git
cd document-converter
docker build -t document-converter .
docker run -p 8000:8080 document-converter
```

Then visit:
- **API Docs**: http://localhost:8000/docs

### Local Development

```bash
git clone https://github.com/YOUR_USERNAME/document-converter.git
cd document-converter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./start-api.sh
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. Clone or download this project
2. Create a virtual environment:

```bash
python3 -m venv .venv
```

3. Activate the virtual environment and install dependencies:

```bash
# On macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt

# Or on Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

Note: WeasyPrint and pdf2image require some system dependencies. If you encounter issues on **macOS**:
```bash
brew install python3 cairo pango gdk-pixbuf libffi poppler
```

On **Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info poppler-utils
```

## Docker Setup (Recommended)

The easiest way to run the Document Converter is using Docker.

```bash
# Build the image
docker build -t document-converter .

# Run the container
docker run -p 8000:8080 document-converter
```

The API will be available at http://localhost:8000

### Stopping the Container

```bash
docker stop $(docker ps -q --filter ancestor=document-converter)
```

## Usage

### Starting the API Server

```bash
./start-api.sh
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### API Endpoints

#### 1. Convert Markdown Content

**POST** `/convert/markdown`

Convert Markdown text to PDF.

```bash
curl -X POST "http://localhost:8000/convert/markdown" \
  -F "content=# Hello World\n\nThis is **markdown**." \
  -F "filename=output.pdf" \
  --output output.pdf
```

**Parameters:**
- `content` (required): Markdown content as string
- `filename` (optional): Output PDF filename (default: document.pdf)
- `custom_css` (optional): Custom CSS styling

#### 2. Convert HTML Content

**POST** `/convert/html`

Convert HTML to PDF.

```bash
curl -X POST "http://localhost:8000/convert/html" \
  -F "content=<h1>Hello</h1><p>This is HTML.</p>" \
  -F "filename=output.pdf" \
  --output output.pdf
```

**Parameters:**
- `content` (required): HTML content as string
- `filename` (optional): Output PDF filename (default: document.pdf)
- `custom_css` (optional): Custom CSS styling

#### 3. Upload and Convert File

**POST** `/convert/file`

Upload a Markdown or HTML file and convert to PDF.

```bash
curl -X POST "http://localhost:8000/convert/file" \
  -F "file=@document.md" \
  --output document.pdf
```

**Parameters:**
- `file` (required): File upload (.md, .markdown, .html, .htm)
- `custom_css` (optional): Custom CSS styling

#### 4. Convert Markdown to Image

**POST** `/convert/markdown/image`

Convert Markdown text to Image (PNG or JPG).

```bash
curl -X POST "http://localhost:8000/convert/markdown/image" \
  -F "content=# Hello World\n\nThis is **markdown**." \
  -F "filename=output.png" \
  -F "image_format=png" \
  --output output.png
```

**Parameters:**
- `content` (required): Markdown content as string
- `filename` (optional): Output image filename (default: document.png)
- `image_format` (optional): png, jpg, or jpeg (default: png)
- `custom_css` (optional): Custom CSS styling
- `width` (optional): Image width in pixels (default: 1200)

#### 5. Convert HTML to Image

**POST** `/convert/html/image`

Convert HTML to Image (PNG or JPG).

```bash
curl -X POST "http://localhost:8000/convert/html/image" \
  -F "content=<h1>Hello</h1><p>This is HTML.</p>" \
  -F "filename=output.jpg" \
  -F "image_format=jpg" \
  --output output.jpg
```

**Parameters:**
- `content` (required): HTML content as string
- `filename` (optional): Output image filename (default: document.png)
- `image_format` (optional): png, jpg, or jpeg (default: png)
- `custom_css` (optional): Custom CSS styling
- `width` (optional): Image width in pixels (default: 1200)

#### 6. Upload and Convert File to Image

**POST** `/convert/file/image`

Upload a Markdown or HTML file and convert to Image.

```bash
curl -X POST "http://localhost:8000/convert/file/image" \
  -F "file=@document.md" \
  -F "image_format=png" \
  --output document.png
```

**Parameters:**
- `file` (required): File upload (.md, .markdown, .html, .htm)
- `image_format` (optional): png, jpg, or jpeg (default: png)
- `custom_css` (optional): Custom CSS styling
- `width` (optional): Image width in pixels (default: 1200)

#### 7. Health Check

**GET** `/health`

Check if the API is running.

```bash
curl http://localhost:8000/health
```

### Python Example

```python
import requests

# Convert Markdown to PDF
markdown_content = "# My Document\n\nThis is **bold** text."

response = requests.post(
    "http://localhost:8000/convert/markdown",
    data={
        "content": markdown_content,
        "filename": "my-document.pdf"
    }
)

with open("my-document.pdf", "wb") as f:
    f.write(response.content)

# Convert Markdown to PNG image
response = requests.post(
    "http://localhost:8000/convert/markdown/image",
    data={
        "content": "# My Image\n\nThis is an image.",
        "filename": "my-image.png",
        "image_format": "png"
    }
)

with open("my-image.png", "wb") as f:
    f.write(response.content)
```

### JavaScript Example

```javascript
// Convert HTML to PDF
const formData = new FormData();
formData.append('content', '<h1>Hello</h1><p>World</p>');
formData.append('filename', 'output.pdf');

fetch('http://localhost:8000/convert/html', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'output.pdf';
    a.click();
});

// Convert Markdown to JPG image
const imageFormData = new FormData();
imageFormData.append('content', '# My Image\n\nConverted to JPG');
imageFormData.append('filename', 'output.jpg');
imageFormData.append('image_format', 'jpg');

fetch('http://localhost:8000/convert/markdown/image', {
    method: 'POST',
    body: imageFormData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'output.jpg';
    a.click();
});
```

### Testing the API

Run the PDF test client:

```bash
.venv/bin/python test-api.py
```

Run the Image test client:

```bash
.venv/bin/python test-image-api.py
```

Or install requests and run:
```bash
pip install requests
python test-api.py
python test-image-api.py
```

### Command-Line Tool (Optional)

You can still use the command-line converter:

```bash
./convert.sh backend/sample.md
./convert.sh backend/sample.html -o output.pdf
```

## PDF Output

The PDFs are generated with:
- **1-inch margins** on all sides (standard document format)
- **Arial font** at 11pt (matching Google Docs default)
- **Proper line spacing** (1.5x) for readability
- **Page numbers** at the bottom center
- **Professional styling** for headings, lists, tables, and code blocks
- **Automatic page breaks** to avoid splitting content awkwardly

## Supported Markdown Features

- Headers (H1-H6)
- Bold, italic, and strikethrough text
- Inline code and code blocks with syntax highlighting
- Ordered and unordered lists
- Tables
- Blockquotes
- Links
- Horizontal rules
- Task lists
- Footnotes

## Customization

The default styling is in `style.css`. You can:

1. Edit this file to change the default styling
2. Create your own CSS file and use it with the `-c` option
3. Modify page size, margins, fonts, colors, and more

### CSS Customization Examples

Change page margins:
```css
@page {
    margin: 0.75in;
}
```

Change font:
```css
body {
    font-family: "Times New Roman", serif;
    font-size: 12pt;
}
```

## Troubleshooting

**Error: "No module named 'fastapi'" or "No module named 'markdown2'"**
- Run: `pip install -r backend/requirements.txt`

**Error: "Failed to load module cairo"**
- Install system dependencies (see Installation section)

**API won't start / Port 8000 in use**
- Change the port in [start-api.sh](start-api.sh): `--port 8001`
- Or kill the process using port 8000

**PDF output looks different than expected**
- Check that `style.css` is in the backend directory
- Try using custom CSS via the `custom_css` parameter

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation where you can test endpoints directly in your browser.

## File Structure

```
document-converter/
├── .github/
│   ├── ISSUE_TEMPLATE/       # Issue templates
│   ├── workflows/            # CI/CD workflows
│   └── pull_request_template.md
├── api.py                    # FastAPI server
├── converter.py              # CLI conversion script
├── style.css                 # Document styling
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── .dockerignore             # Docker ignore patterns
├── start-api.sh              # Start API server script
├── convert.sh                # CLI convenience script
├── LICENSE                   # MIT License
├── CONTRIBUTING.md           # Contribution guidelines
├── CODE_OF_CONDUCT.md        # Code of conduct
├── SECURITY.md               # Security policy
├── CHANGELOG.md              # Version history
└── README.md                 # This file
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Development setup
- Code style guidelines

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Security

For security concerns, please see our [Security Policy](SECURITY.md).

## Support

- 📖 [API Documentation](http://localhost:8000/docs)
- 🐛 [Report a Bug](.github/ISSUE_TEMPLATE/bug_report.md)
- 💡 [Request a Feature](.github/ISSUE_TEMPLATE/feature_request.md)
- 💬 Open a [GitHub Issue](../../issues)

## Roadmap

- [ ] Batch conversion support
- [ ] Webhook notifications
- [ ] Template system for custom styling
- [ ] Cloud storage integrations
- [ ] PDF encryption and password protection

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [WeasyPrint](https://weasyprint.org/) - PDF rendering
- [pdf2image](https://github.com/Belval/pdf2image) - PDF to image conversion
- [markdown2](https://github.com/trentm/python-markdown2) - Markdown processing

---

<div align="center">
  <sub>Built with ❤️ by the Document Converter community</sub>
</div>
