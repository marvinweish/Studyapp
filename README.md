# AI Study Buddy

A Python application built with Flet that helps you study by converting various document formats into interactive flashcards.

## Features

- **Multi-format Support**: Upload documents in various formats:
  - Text files (.txt)
  - PDF documents (.pdf)
  - Word documents (.docx, .doc)
  - PowerPoint presentations (.pptx, .ppt)
  - EPUB books (.epub)
- **Intelligent Chapter Detection**: Automatically parse and organize content into chapters or sections
- **Interactive Flashcards**: Generate and study with interactive flashcards
- **Modern UI**: Dark theme interface built with Flet
- **Content Organization**: Smart content parsing and topic extraction

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python study_app.py
```

## Testing File Processing

Test the file processor with different document formats:

```bash
python test_file_processor.py sample_book.txt
```

## Usage

1. **Upload a Document**: Click the upload button in the app bar to upload a document
2. **Select Content**: Choose from automatically detected chapters or sections
3. **Study Method**: Select "Flashcards" as your study method
4. **Interactive Learning**: Use navigation buttons and flip cards to study

## File Processing Capabilities

The application uses a sophisticated file processing system that:

- **Extracts text content** from various document formats
- **Detects chapter structures** using multiple pattern recognition methods
- **Organizes content** into logical sections for studying
- **Handles metadata** like titles, authors, and document properties
- **Provides fallback methods** for documents without clear chapter structure

## Dependencies

### Core Dependencies
- `flet`: Cross-platform app framework for Python

### File Processing Dependencies
- `PyPDF2`: PDF document processing
- `python-docx`: Word document processing  
- `python-pptx`: PowerPoint presentation processing
- `ebooklib`: EPUB book processing
- `beautifulsoup4`: HTML parsing for EPUB files

## Architecture

- `study_app.py`: Main application interface and logic
- `file_processor.py`: Document processing and content organization
- `test_file_processor.py`: Testing utilities for file processing

## Supported Study Methods

- ✅ **Flashcards**: Interactive term/definition cards with flip animations
- 🔄 **Quiz**: Multiple choice questions (Coming Soon)
- 🔄 **Test**: Comprehensive testing features (Coming Soon)
