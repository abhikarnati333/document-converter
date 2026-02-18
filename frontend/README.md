# Document Converter Frontend

A modern, responsive web interface for the Document Converter API.

## Features

- 🎨 **Modern UI Design** - Clean, professional interface with smooth animations
- 📁 **File Upload** - Drag & drop or browse to upload HTML/Markdown files
- ✍️ **Text Input** - Paste content directly for quick conversions
- 🔄 **Multiple Formats** - Convert to PDF, PNG, or JPG
- ⚙️ **Customizable** - Adjust image dimensions for PNG/JPG outputs
- 📱 **Responsive** - Works seamlessly on desktop, tablet, and mobile
- 🚀 **Real-time Feedback** - Progress indicators and instant downloads
- ❌ **Error Handling** - Clear error messages with retry options

## Quick Start

### 1. Start the Backend API

Make sure the backend API is running on `http://localhost:8000`:

```bash
cd backend
source ../.venv/bin/activate
uvicorn api:app --reload
```

### 2. Open the Frontend

Simply open `index.html` in your web browser:

```bash
# Option 1: Open directly
open frontend/index.html

# Option 2: Use Python's built-in server
cd frontend
python3 -m http.server 8080
# Then visit: http://localhost:8080
```

## Usage Guide

### File Upload Method

1. Click the **"Upload File"** tab (default)
2. Drag & drop your file or click to browse
3. Select output format (PDF, PNG, or JPG)
4. For images, adjust dimensions if needed
5. Click **"Convert Document"**
6. Download your converted file

**Supported file types:** `.html`, `.md`, `.markdown`

### Text Input Method

1. Click the **"Paste Content"** tab
2. Select input format (Markdown or HTML)
3. Paste your content into the text area
4. Select output format (PDF, PNG, or JPG)
5. For images, adjust dimensions if needed
6. Click **"Convert Document"**
7. Download your converted file

## Output Formats

### PDF
- Google Docs-style formatting
- Proper page breaks and pagination
- Professional typography
- 1-inch margins

### PNG
- High-quality raster images
- Transparent backgrounds supported
- Multi-page documents combined vertically
- Default: 1275×1650px per page

### JPG
- Optimized file sizes
- Perfect for web sharing
- Multi-page documents combined vertically
- Default: 1275×1650px per page

## Customization

### Image Dimensions

When converting to PNG or JPG, you can customize:
- **Width**: 100-4000 pixels (default: 1275px)
- **Height**: 100-8000 pixels (default: 1650px)

**Note:** Multi-page documents are automatically combined into a single tall image.

### API Configuration

To use a different API endpoint, edit `frontend/js/api.js`:

```javascript
const API_BASE_URL = 'http://your-api-url.com';
```

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Troubleshooting

### API Connection Failed

**Error:** "Cannot connect to the API"

**Solution:**
1. Make sure the backend API is running on `http://localhost:8000`
2. Check if the API is accessible: visit `http://localhost:8000/docs`
3. Verify CORS is enabled in the backend

### File Upload Not Working

**Error:** "Invalid file type"

**Solution:**
- Ensure your file has a `.html`, `.md`, or `.markdown` extension
- Check that the file is not corrupted
- Try pasting the content into the text input method instead

### Conversion Failed

**Error:** Various conversion errors

**Solution:**
1. Verify your content is valid HTML or Markdown
2. Check the browser console for detailed error messages
3. Try converting a simple test document first
4. Review the API logs in the terminal

### Download Not Starting

**Issue:** Download button doesn't work

**Solution:**
1. Check your browser's download settings
2. Ensure pop-ups are not blocked
3. Try a different browser
4. Check browser console for errors

## Project Structure

```
frontend/
├── index.html          # Main HTML interface
├── css/
│   └── styles.css      # All styling and responsive design
├── js/
│   ├── api.js          # API communication module
│   └── app.js          # Main application logic
├── assets/             # Images and icons (if needed)
└── README.md           # This file
```

## Development

### Local Testing

For development, it's recommended to use a local server to avoid CORS issues:

```bash
# Using Python
cd frontend
python3 -m http.server 8080

# Using Node.js (if you have http-server installed)
cd frontend
npx http-server -p 8080
```

Then visit: `http://localhost:8080`

### Making Changes

1. **HTML Changes:** Edit `index.html` for structure
2. **Style Changes:** Edit `css/styles.css` for appearance
3. **Logic Changes:** Edit `js/app.js` for UI behavior
4. **API Changes:** Edit `js/api.js` for backend communication

All changes take effect immediately - just refresh your browser!

## Performance Tips

- For large files, file upload is faster than text input
- PNG files are larger but higher quality than JPG
- Reduce image dimensions for faster conversions
- Use JPG format for smaller file sizes

## Security Notes

- File uploads are processed server-side
- No data is stored permanently
- All conversions happen in-memory
- CORS is enabled for localhost development

## Need Help?

- **API Documentation:** Visit `http://localhost:8000/docs`
- **Backend Issues:** Check the backend terminal for logs
- **Frontend Issues:** Open browser DevTools Console (F12)

## License

This frontend is part of the Document Converter project.
