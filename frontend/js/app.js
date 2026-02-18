/**
 * Main Application Logic
 * Handles UI interactions, file management, and conversion orchestration
 */

// Application State
const state = {
    currentTab: 'file',
    selectedFile: null,
    outputFormat: 'pdf',
    inputFormat: 'markdown',
    imageWidth: 1275,
    imageHeight: 1650,
    convertedBlob: null,
    convertedFileName: null
};

// DOM Elements
const elements = {
    // Tabs
    tabButtons: document.querySelectorAll('.tab-button'),
    tabContents: document.querySelectorAll('.tab-content'),
    
    // File Upload
    uploadArea: document.getElementById('upload-area'),
    fileInput: document.getElementById('file-input'),
    fileInfo: document.getElementById('file-info'),
    removeFileBtn: document.getElementById('remove-file-btn'),
    
    // Text Input
    textInput: document.getElementById('text-input'),
    inputFormatRadios: document.querySelectorAll('input[name="input-format"]'),
    
    // Format Selection
    formatButtons: document.querySelectorAll('.format-btn'),
    imageOptions: document.getElementById('image-options'),
    imageWidth: document.getElementById('image-width'),
    imageHeight: document.getElementById('image-height'),
    
    // Actions
    convertBtn: document.getElementById('convert-btn'),
    
    // Progress
    progressContainer: document.getElementById('progress-container'),
    progressFill: document.getElementById('progress-fill'),
    progressText: document.getElementById('progress-text'),
    
    // Results
    resultArea: document.getElementById('result-area'),
    resultMessage: document.getElementById('result-message'),
    downloadBtn: document.getElementById('download-btn'),
    convertAnotherBtn: document.getElementById('convert-another-btn'),
    
    // Error
    errorArea: document.getElementById('error-area'),
    errorMessage: document.getElementById('error-message'),
    tryAgainBtn: document.getElementById('try-again-btn')
};

/**
 * Initialize the application
 */
function init() {
    setupTabSwitching();
    setupFileUpload();
    setupTextInput();
    setupFormatSelection();
    setupConversion();
    setupResultActions();
    checkAPIHealth();
}

/**
 * Setup tab switching between file upload and text input
 */
function setupTabSwitching() {
    elements.tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

/**
 * Switch to a specific tab
 */
function switchTab(tabName) {
    state.currentTab = tabName;
    
    // Update tab buttons
    elements.tabButtons.forEach(btn => {
        if (btn.getAttribute('data-tab') === tabName) {
            btn.setAttribute('data-active', 'true');
        } else {
            btn.setAttribute('data-active', 'false');
        }
    });
    
    // Update tab content
    elements.tabContents.forEach(content => {
        if (content.id === `${tabName}-tab`) {
            content.classList.remove('hidden');
        } else {
            content.classList.add('hidden');
        }
    });
    
    resetUI();
}

/**
 * Setup file upload functionality
 */
function setupFileUpload() {
    // Click to browse
    elements.uploadArea.addEventListener('click', () => {
        elements.fileInput.click();
    });
    
    // File selection
    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
    
    // Drag and drop
    elements.uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.add('drag-over');
    });
    
    elements.uploadArea.addEventListener('dragleave', () => {
        elements.uploadArea.classList.remove('drag-over');
    });
    
    elements.uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });
    
    // Remove file
    elements.removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        clearFileSelection();
    });
}

/**
 * Handle file selection
 */
function handleFileSelection(file) {
    // Validate file type
    const validExtensions = ['.html', '.md', '.markdown'];
    const fileName = file.name.toLowerCase();
    const isValid = validExtensions.some(ext => fileName.endsWith(ext));
    
    if (!isValid) {
        showError('Invalid file type. Please upload .html, .md, or .markdown files.');
        return;
    }
    
    state.selectedFile = file;
    
    // Update UI
    elements.uploadArea.classList.add('hidden');
    elements.fileInfo.classList.remove('hidden');
    elements.fileInfo.querySelector('.file-name').textContent = file.name;
    elements.fileInfo.querySelector('.file-size').textContent = formatFileSize(file.size);
}

/**
 * Clear file selection
 */
function clearFileSelection() {
    state.selectedFile = null;
    elements.fileInput.value = '';
    elements.uploadArea.classList.remove('hidden');
    elements.fileInfo.classList.add('hidden');
}

/**
 * Setup text input functionality
 */
function setupTextInput() {
    elements.inputFormatRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            state.inputFormat = e.target.value;
            updateTextInputPlaceholder();
        });
    });
}

/**
 * Update text input placeholder based on selected format
 */
function updateTextInputPlaceholder() {
    const placeholders = {
        markdown: `Paste your Markdown content here...

Example Markdown:
# Heading
**Bold text** and *italic text*
- List item 1
- List item 2`,
        html: `Paste your HTML content here...

Example HTML:
<!DOCTYPE html>
<html>
<head><title>Document</title></head>
<body>
    <h1>Heading</h1>
    <p>Paragraph text</p>
</body>
</html>`
    };
    
    elements.textInput.placeholder = placeholders[state.inputFormat];
}

/**
 * Setup format selection
 */
function setupFormatSelection() {
    elements.formatButtons.forEach(button => {
        button.addEventListener('click', () => {
            const format = button.getAttribute('data-format');
            selectFormat(format);
        });
    });
    
    // Image dimension inputs
    elements.imageWidth.addEventListener('change', (e) => {
        state.imageWidth = parseInt(e.target.value) || 1275;
    });
    
    elements.imageHeight.addEventListener('change', (e) => {
        state.imageHeight = parseInt(e.target.value) || 1650;
    });
}

/**
 * Select output format
 */
function selectFormat(format) {
    state.outputFormat = format;
    
    // Update button states
    elements.formatButtons.forEach(btn => {
        if (btn.getAttribute('data-format') === format) {
            btn.setAttribute('data-active', 'true');
        } else {
            btn.setAttribute('data-active', 'false');
        }
    });
    
    // Show/hide image options
    if (format === 'png' || format === 'jpg') {
        elements.imageOptions.classList.remove('hidden');
    } else {
        elements.imageOptions.classList.add('hidden');
    }
}

/**
 * Setup conversion process
 */
function setupConversion() {
    elements.convertBtn.addEventListener('click', handleConversion);
}

/**
 * Handle the conversion process
 */
async function handleConversion() {
    try {
        // Validate input
        if (state.currentTab === 'file' && !state.selectedFile) {
            showError('Please select a file to convert');
            return;
        }
        
        if (state.currentTab === 'text' && !elements.textInput.value.trim()) {
            showError('Please enter content to convert');
            return;
        }
        
        // Show progress
        showProgress();
        
        // Prepare conversion options
        const options = {
            outputFormat: state.outputFormat,
            width: state.imageWidth,
            height: state.imageHeight
        };
        
        if (state.currentTab === 'file') {
            options.file = state.selectedFile;
        } else {
            options.content = elements.textInput.value;
            options.inputFormat = state.inputFormat;
        }
        
        // Perform conversion
        const blob = await api.convert(options);
        
        // Check if the result is a zip file (multi-page images)
        const isZip = blob.type === 'application/zip' || blob.type === 'application/x-zip-compressed';
        
        // Generate filename
        const timestamp = new Date().toISOString().split('T')[0];
        const baseName = state.selectedFile ? 
            state.selectedFile.name.replace(/\.[^/.]+$/, '') : 
            'document';
        
        // Use .zip extension if it's a zip file, otherwise use the output format
        const extension = isZip ? 'zip' : state.outputFormat;
        const fileName = `${baseName}-${timestamp}.${extension}`;
        
        // Store result
        state.convertedBlob = blob;
        state.convertedFileName = fileName;
        
        // Show success
        showSuccess(fileName);
        
    } catch (error) {
        console.error('Conversion error:', error);
        showError(error.message || 'An error occurred during conversion');
    }
}

/**
 * Setup result action buttons
 */
function setupResultActions() {
    elements.downloadBtn.addEventListener('click', downloadResult);
    elements.convertAnotherBtn.addEventListener('click', resetForNewConversion);
    elements.tryAgainBtn.addEventListener('click', resetForNewConversion);
}

/**
 * Download the converted result
 */
function downloadResult() {
    if (!state.convertedBlob || !state.convertedFileName) {
        return;
    }
    
    const url = URL.createObjectURL(state.convertedBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = state.convertedFileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * Reset for a new conversion
 */
function resetForNewConversion() {
    resetUI();
    
    // Clear inputs
    if (state.currentTab === 'file') {
        clearFileSelection();
    } else {
        elements.textInput.value = '';
    }
    
    // Clear result
    state.convertedBlob = null;
    state.convertedFileName = null;
}

/**
 * Show progress indicator
 */
function showProgress() {
    elements.convertBtn.disabled = true;
    elements.progressContainer.classList.remove('hidden');
    elements.resultArea.classList.add('hidden');
    elements.errorArea.classList.add('hidden');
    
    elements.progressText.textContent = `Converting to ${state.outputFormat.toUpperCase()}...`;
}

/**
 * Show success message
 */
function showSuccess(fileName) {
    elements.convertBtn.disabled = false;
    elements.progressContainer.classList.add('hidden');
    elements.resultArea.classList.remove('hidden');
    elements.errorArea.classList.add('hidden');
    
    const formatName = state.outputFormat.toUpperCase();
    
    // Check if it's a zip file (multi-page images)
    if (fileName.endsWith('.zip')) {
        elements.resultMessage.textContent = `Your multi-page document has been converted to ${formatName} images (ZIP file)`;
    } else {
        elements.resultMessage.textContent = `Your document has been converted to ${formatName}`;
    }
}

/**
 * Show error message
 */
function showError(message) {
    elements.convertBtn.disabled = false;
    elements.progressContainer.classList.add('hidden');
    elements.resultArea.classList.add('hidden');
    elements.errorArea.classList.remove('hidden');
    
    elements.errorMessage.textContent = message;
}

/**
 * Reset UI to initial state
 */
function resetUI() {
    elements.convertBtn.disabled = false;
    elements.progressContainer.classList.add('hidden');
    elements.resultArea.classList.add('hidden');
    elements.errorArea.classList.add('hidden');
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

/**
 * Check API health on startup
 */
async function checkAPIHealth() {
    try {
        await api.checkHealth();
        console.log('✓ API is healthy and ready');
    } catch (error) {
        console.error('⚠ API health check failed:', error);
        showError('Cannot connect to the API. Make sure the backend server is running on http://localhost:8000');
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
