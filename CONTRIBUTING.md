# Contributing to Document Converter

Thank you for your interest in contributing! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, browser)
- Any relevant logs or error messages

### Suggesting Features

We love feature suggestions! Please open an issue with:
- A clear description of the feature
- Why this feature would be useful
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes**:
   - Write clear, concise commit messages
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
3. **Test your changes**:
   - Ensure the API works correctly
   - Test with different file formats
   - Check both PDF and image outputs
4. **Submit a pull request**:
   - Link any related issues
   - Describe what your PR does
   - Include screenshots for UI changes

## Development Setup

### Prerequisites
- Python 3.9+
- Docker (optional, for containerized development)

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/document-converter.git
cd document-converter

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
./start-api.sh
```

### Using Docker

```bash
docker-compose up -d
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Testing

Before submitting a PR:
- Test API endpoints manually or with test scripts
- Try different file formats (Markdown, HTML)
- Test both PDF and image conversions
- Verify multi-page documents work correctly

## Documentation

- Update README.md if you add features or change usage
- Add comments for complex code
- Update API documentation for new endpoints

## Questions?

Feel free to open an issue for any questions about contributing!

## Code of Conduct

Be respectful, inclusive, and professional. We're all here to build something great together.
