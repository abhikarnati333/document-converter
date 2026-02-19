#!/usr/bin/env python3
"""
Document Converter - Convert HTML and Markdown files to Google Docs-styled PDFs
"""

import argparse
import os
import sys
from pathlib import Path
import markdown2
from weasyprint import HTML, CSS


def read_file(file_path):
    """Read content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)


def markdown_to_html(markdown_content):
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
    return html


def wrap_html_with_template(body_html):
    """Wrap HTML content with a complete document template."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {body_html}
</body>
</html>"""


def convert_to_pdf(html_content, output_path, css_path=None):
    """Convert HTML content to PDF with Google Docs styling."""
    try:
        # Determine which CSS file to use
        css_files = []
        if css_path and os.path.exists(css_path):
            css_files.append(css_path)
        else:
            # Use default CSS if it exists
            default_css = os.path.join(os.path.dirname(__file__), 'google-docs-style.css')
            if os.path.exists(default_css):
                css_files.append(default_css)
        
        # Create PDF with CSS
        html_obj = HTML(string=html_content)
        if css_files:
            stylesheets = [CSS(filename=css_file) for css_file in css_files]
            html_obj.write_pdf(output_path, stylesheets=stylesheets)
        else:
            html_obj.write_pdf(output_path)
        
        print(f"✓ PDF created successfully: {output_path}")
        return True
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert HTML or Markdown files to Google Docs-styled PDFs'
    )
    parser.add_argument(
        'input_file',
        help='Input file (HTML or Markdown)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output PDF file path (default: same name as input with .pdf extension)'
    )
    parser.add_argument(
        '-c', '--css',
        help='Custom CSS file for styling (optional)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    
    # Determine output file path
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input_file)
        output_path = input_path.with_suffix('.pdf')
    
    # Read input file
    print(f"Reading {args.input_file}...")
    content = read_file(args.input_file)
    
    # Determine file type and convert to HTML
    file_ext = Path(args.input_file).suffix.lower()
    
    if file_ext in ['.md', '.markdown']:
        print("Converting Markdown to HTML...")
        html_body = markdown_to_html(content)
        html_content = wrap_html_with_template(html_body)
    elif file_ext in ['.html', '.htm']:
        print("Processing HTML...")
        # Check if it's a complete HTML document or just a fragment
        if '<html' in content.lower():
            html_content = content
        else:
            html_content = wrap_html_with_template(content)
    else:
        print(f"Error: Unsupported file type '{file_ext}'. Supported: .md, .markdown, .html, .htm")
        sys.exit(1)
    
    # Convert to PDF
    print("Generating PDF...")
    success = convert_to_pdf(html_content, output_path, args.css)
    
    if success:
        print(f"\n✓ Conversion complete!")
        print(f"  Input:  {args.input_file}")
        print(f"  Output: {output_path}")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
