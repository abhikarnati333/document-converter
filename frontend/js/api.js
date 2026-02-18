/**
 * API Communication Module
 * Handles all requests to the Document Converter API
 */

class DocumentConverterAPI {
    constructor(baseURL = null) {
        this.baseURL = baseURL || window.CONFIG?.API_BASE_URL || 'http://localhost:8000';
    }

    /**
     * Convert Markdown text to PDF
     * @param {string} markdownContent - The Markdown content to convert
     * @returns {Promise<Blob>} - PDF file as Blob
     */
    async markdownToPDF(markdownContent) {
        const response = await fetch(`${this.baseURL}/convert/markdown/pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ markdown: markdownContent })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to convert Markdown to PDF');
        }

        return await response.blob();
    }

    /**
     * Convert HTML text to PDF
     * @param {string} htmlContent - The HTML content to convert
     * @returns {Promise<Blob>} - PDF file as Blob
     */
    async htmlToPDF(htmlContent) {
        const response = await fetch(`${this.baseURL}/convert/html/pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ html: htmlContent })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to convert HTML to PDF');
        }

        return await response.blob();
    }

    /**
     * Convert Markdown text to Image (PNG/JPG)
     * @param {string} markdownContent - The Markdown content to convert
     * @param {string} imageFormat - 'png' or 'jpg'
     * @param {number} width - Image width in pixels
     * @param {number} height - Image height in pixels
     * @returns {Promise<Blob>} - Image file as Blob
     */
    async markdownToImage(markdownContent, imageFormat = 'png', width = 1275, height = 1650) {
        const response = await fetch(`${this.baseURL}/convert/markdown/image`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                markdown: markdownContent,
                image_format: imageFormat,
                width: width,
                height: height
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `Failed to convert Markdown to ${imageFormat.toUpperCase()}`);
        }

        return await response.blob();
    }

    /**
     * Convert HTML text to Image (PNG/JPG)
     * @param {string} htmlContent - The HTML content to convert
     * @param {string} imageFormat - 'png' or 'jpg'
     * @param {number} width - Image width in pixels
     * @param {number} height - Image height in pixels
     * @returns {Promise<Blob>} - Image file as Blob
     */
    async htmlToImage(htmlContent, imageFormat = 'png', width = 1275, height = 1650) {
        const response = await fetch(`${this.baseURL}/convert/html/image`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                html: htmlContent,
                image_format: imageFormat,
                width: width,
                height: height
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `Failed to convert HTML to ${imageFormat.toUpperCase()}`);
        }

        return await response.blob();
    }

    /**
     * Convert uploaded file (HTML or Markdown) to PDF
     * @param {File} file - The file to convert
     * @returns {Promise<Blob>} - PDF file as Blob
     */
    async fileToPDF(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${this.baseURL}/convert/file`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to convert file to PDF');
        }

        return await response.blob();
    }

    /**
     * Convert uploaded file (HTML or Markdown) to Image
     * @param {File} file - The file to convert
     * @param {string} imageFormat - 'png' or 'jpg'
     * @param {number} width - Image width in pixels
     * @param {number} height - Image height in pixels
     * @returns {Promise<Blob>} - Image file as Blob
     */
    async fileToImage(file, imageFormat = 'png', width = 1275, height = 1650) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('image_format', imageFormat);
        formData.append('width', width.toString());
        formData.append('height', height.toString());

        const response = await fetch(`${this.baseURL}/convert/file/image`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `Failed to convert file to ${imageFormat.toUpperCase()}`);
        }

        return await response.blob();
    }

    /**
     * Check API health status
     * @returns {Promise<object>} - Health status object
     */
    async checkHealth() {
        const response = await fetch(`${this.baseURL}/health`);

        if (!response.ok) {
            throw new Error('API health check failed');
        }

        return await response.json();
    }

    /**
     * Generic conversion method that routes to the appropriate API call
     * @param {object} options - Conversion options
     * @returns {Promise<Blob>} - Converted file as Blob
     */
    async convert(options) {
        const {
            content,
            file,
            inputFormat,
            outputFormat,
            width = 1275,
            height = 1650
        } = options;

        // File upload conversion
        if (file) {
            if (outputFormat === 'pdf') {
                return await this.fileToPDF(file);
            } else {
                return await this.fileToImage(file, outputFormat, width, height);
            }
        }

        // Text content conversion
        if (content) {
            if (outputFormat === 'pdf') {
                if (inputFormat === 'markdown') {
                    return await this.markdownToPDF(content);
                } else {
                    return await this.htmlToPDF(content);
                }
            } else {
                if (inputFormat === 'markdown') {
                    return await this.markdownToImage(content, outputFormat, width, height);
                } else {
                    return await this.htmlToImage(content, outputFormat, width, height);
                }
            }
        }

        throw new Error('Either content or file must be provided');
    }
}

// Export a single instance
const api = new DocumentConverterAPI();
