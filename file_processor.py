"""
File Processing Module for AI Study Buddy

This module handles the processing of various file formats including:
- PDF (.pdf)
- Word Documents (.docx, .doc)
- PowerPoint Presentations (.pptx, .ppt)
- EPUB files (.epub)
- Text files (.txt)

The module extracts text content and organizes it into chapters or topics
for use by the flashcards, quiz, and test functions.
"""

import os
import re
import zipfile
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

# Optional imports - will be installed as needed
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from pptx import Presentation
    PPTX_AVAILABLE = True
except ImportError:
    PPTX_AVAILABLE = False

try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    EPUB_AVAILABLE = True
except ImportError:
    EPUB_AVAILABLE = False

# OCR support for image-based PDFs
try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    
    # Configure Tesseract path for Windows
    import platform
    if platform.system() == "Windows":
        # Try common installation paths for Tesseract
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\Admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        ]
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
        
        # Configure poppler path for pdf2image
        poppler_paths = [
            r"C:\poppler\poppler-21.11.0\Library\bin",
            r"C:\poppler\Library\bin",
            r"C:\Program Files\poppler\bin"
        ]
        for path in poppler_paths:
            if os.path.exists(path):
                os.environ["PATH"] = path + ";" + os.environ.get("PATH", "")
                break
    
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


@dataclass
class ProcessedContent:
    """Represents processed content from a file"""
    title: str
    content: str
    file_type: str
    metadata: Optional[Dict] = None


@dataclass
class Chapter:
    """Represents a chapter or section in the processed content"""
    title: str
    content: str
    index: int
    subsections: Optional[List['Chapter']] = None


class FileProcessor:
    """Main class for processing various file formats"""
    
    SUPPORTED_EXTENSIONS = {
        '.txt': 'text',
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.doc': 'doc',
        '.pptx': 'pptx',
        '.ppt': 'ppt',
        '.epub': 'epub'
    }
    
    def __init__(self):
        self.missing_dependencies = self._check_dependencies()
    
    def _check_dependencies(self) -> List[str]:
        """Check which dependencies are missing"""
        missing = []
        if not PDF_AVAILABLE:
            missing.append("PyPDF2")
        if not DOCX_AVAILABLE:
            missing.append("python-docx")
        if not PPTX_AVAILABLE:
            missing.append("python-pptx")
        if not EPUB_AVAILABLE:
            missing.extend(["ebooklib", "beautifulsoup4"])
        if not OCR_AVAILABLE:
            missing.extend(["pytesseract", "pdf2image", "Pillow"])
        return missing
    
    def get_missing_dependencies(self) -> List[str]:
        """Return list of missing dependencies"""
        return self.missing_dependencies
    
    def is_supported(self, file_path: str) -> bool:
        """Check if file format is supported"""
        ext = Path(file_path).suffix.lower()
        return ext in self.SUPPORTED_EXTENSIONS
    
    def process_file(self, file_path: str) -> ProcessedContent:
        """Main method to process any supported file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        ext = Path(file_path).suffix.lower()
        if not self.is_supported(file_path):
            raise ValueError(f"Unsupported file format: {ext}")
        
        file_type = self.SUPPORTED_EXTENSIONS[ext]
        
        # Route to appropriate processor
        if file_type == 'text':
            return self._process_txt(file_path)
        elif file_type == 'pdf':
            return self._process_pdf(file_path)
        elif file_type in ['docx', 'doc']:
            return self._process_docx(file_path)
        elif file_type in ['pptx', 'ppt']:
            return self._process_pptx(file_path)
        elif file_type == 'epub':
            return self._process_epub(file_path)
        else:
            raise ValueError(f"No processor available for {file_type}")
    
    def _process_txt(self, file_path: str) -> ProcessedContent:
        """Process text files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        return ProcessedContent(
            title=Path(file_path).stem,
            content=content,
            file_type='text'
        )
    
    def _process_pdf(self, file_path: str) -> ProcessedContent:
        """Process PDF files with OCR fallback for image-based PDFs"""
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 is required for PDF processing. Install with: pip install PyPDF2")
        
        content = []
        metadata = {}
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'pages': len(pdf_reader.pages)
                    }
                
                # First, try to extract text normally
                extracted_text = []
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        if text.strip():
                            extracted_text.append(text.strip())
                    except Exception as e:
                        print(f"Error extracting text from page {page_num + 1}: {e}")
                
                # Check if we got meaningful text (more than just spaces/newlines)
                total_text = ' '.join(extracted_text)
                meaningful_text = re.sub(r'\s+', ' ', total_text).strip()
                
                # If we have very little meaningful text, try OCR
                if len(meaningful_text) < 100:  # Less than 100 characters suggests image-based PDF
                    print("PDF appears to be image-based. Attempting OCR...")
                    if OCR_AVAILABLE:
                        try:
                            content = self._process_pdf_with_ocr(file_path)
                        except Exception as ocr_error:
                            print(f"OCR failed: {ocr_error}")
                            # Fall back to whatever text we could extract
                            content = [f"--- Page {i+1} ---\n{text}" for i, text in enumerate(extracted_text) if text.strip()]
                            if not content:
                                content = ["No readable text found in this PDF. This may be an image-based PDF that requires OCR."]
                    else:
                        content = ["No readable text found. This appears to be an image-based PDF. Install OCR dependencies with: pip install pytesseract pdf2image pillow"]
                else:
                    # We have good text extraction, format it
                    content = [f"--- Page {i+1} ---\n{text}" for i, text in enumerate(extracted_text) if text.strip()]
        
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")
        
        return ProcessedContent(
            title=metadata.get('title', Path(file_path).stem),
            content='\n\n'.join(content),
            file_type='pdf',
            metadata=metadata
        )
    
    def _process_pdf_with_ocr(self, file_path: str) -> List[str]:
        """Process PDF using OCR for image-based PDFs"""
        if not OCR_AVAILABLE:
            raise ImportError("OCR dependencies required. Install with: pip install pytesseract pdf2image pillow")
        
        try:
            # Convert PDF pages to images
            images = convert_from_path(file_path)
            content = []
            
            for page_num, image in enumerate(images):
                try:
                    # Use OCR to extract text from image
                    text = pytesseract.image_to_string(image, lang='eng')
                    if text.strip():
                        content.append(f"--- Page {page_num + 1} (OCR) ---\n{text.strip()}")
                    else:
                        content.append(f"--- Page {page_num + 1} (OCR) ---\nNo text detected on this page")
                except Exception as e:
                    content.append(f"--- Page {page_num + 1} (OCR Error) ---\nError: {str(e)}")
            
            return content
        
        except Exception as e:
            raise ValueError(f"OCR processing failed: {str(e)}")
    
    def _process_docx(self, file_path: str) -> ProcessedContent:
        """Process Word documents"""
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx is required for DOCX processing. Install with: pip install python-docx")
        
        try:
            doc = Document(file_path)
            content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    # Check if it's a heading
                    if paragraph.style.name.startswith('Heading'):
                        content.append(f"\n{paragraph.text}\n" + "=" * len(paragraph.text))
                    else:
                        content.append(paragraph.text)
            
            return ProcessedContent(
                title=Path(file_path).stem,
                content='\n\n'.join(content),
                file_type='docx'
            )
        
        except Exception as e:
            raise ValueError(f"Error processing DOCX: {str(e)}")
    
    def _process_pptx(self, file_path: str) -> ProcessedContent:
        """Process PowerPoint presentations"""
        if not PPTX_AVAILABLE:
            raise ImportError("python-pptx is required for PPTX processing. Install with: pip install python-pptx")
        
        try:
            prs = Presentation(file_path)
            content = []
            
            for slide_num, slide in enumerate(prs.slides, 1):
                slide_content = [f"--- Slide {slide_num} ---"]
                
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        slide_content.append(shape.text)
                
                if len(slide_content) > 1:  # More than just the slide header
                    content.append('\n'.join(slide_content))
            
            return ProcessedContent(
                title=Path(file_path).stem,
                content='\n\n'.join(content),
                file_type='pptx'
            )
        
        except Exception as e:
            raise ValueError(f"Error processing PPTX: {str(e)}")
    
    def _process_epub(self, file_path: str) -> ProcessedContent:
        """Process EPUB files"""
        if not EPUB_AVAILABLE:
            raise ImportError("ebooklib and beautifulsoup4 are required for EPUB processing. Install with: pip install ebooklib beautifulsoup4")
        
        try:
            book = epub.read_epub(file_path)
            content = []
            metadata = {}
            
            # Extract metadata
            metadata['title'] = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else ''
            metadata['author'] = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else ''
            
            # Extract text content
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text = soup.get_text()
                    if text.strip():
                        content.append(text)
            
            return ProcessedContent(
                title=metadata.get('title', Path(file_path).stem),
                content='\n\n'.join(content),
                file_type='epub',
                metadata=metadata
            )
        
        except Exception as e:
            raise ValueError(f"Error processing EPUB: {str(e)}")
    
    def _process_image_based_pdf(self, file_path: str) -> ProcessedContent:
        """Process image-based PDF files using OCR"""
        if not OCR_AVAILABLE:
            raise ImportError("pytesseract, pdf2image, and Pillow are required for OCR processing. Install with: pip install pytesseract pdf2image Pillow")
        
        content = []
        metadata = {}
        
        try:
            # Convert PDF pages to images
            images = convert_from_path(file_path)
            
            for i, image in enumerate(images):
                # Perform OCR on the image
                text = pytesseract.image_to_string(image)
                if text.strip():
                    content.append(f"--- Page {i + 1} ---\n{text}")
        
        except Exception as e:
            raise ValueError(f"Error processing image-based PDF: {str(e)}")
        
        return ProcessedContent(
            title=Path(file_path).stem,
            content='\n\n'.join(content),
            file_type='pdf',
            metadata=metadata
        )


class ContentOrganizer:
    """Organizes processed content into chapters and topics"""
    
    def __init__(self):
        self.chapter_patterns = [
            r'^(Chapter\s+\d+[:\-\s]*.*?)$',
            r'^(CHAPTER\s+\d+[:\-\s]*.*?)$',
            r'^(\d+\.\s*.*?)$',
            r'^(Part\s+\d+[:\-\s]*.*?)$',
            r'^(Section\s+\d+[:\-\s]*.*?)$',
            r'^(Unit\s+\d+[:\-\s]*.*?)$',
        ]
    
    def organize_into_chapters(self, content: ProcessedContent, min_chapter_length: int = 500) -> List[Chapter]:
        """Organize content into chapters based on patterns"""
        text = content.content
        chapters = []
        
        # Try to find chapters using patterns
        found_chapters = self._find_chapters_by_pattern(text)
        
        if found_chapters:
            for i, (title, chapter_content) in enumerate(found_chapters):
                if len(chapter_content.strip()) >= min_chapter_length:
                    chapters.append(Chapter(
                        title=title.strip(),
                        content=chapter_content.strip(),
                        index=i
                    ))
        else:
            # If no chapters found, split by length or use whole content
            chapters = self._split_by_length(content, min_chapter_length)
        
        return chapters
    
    def _find_chapters_by_pattern(self, text: str) -> List[tuple]:
        """Find chapters using regex patterns"""
        for pattern in self.chapter_patterns:
            matches = list(re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE))
            if matches:
                return self._extract_chapters_from_matches(text, matches)
        return []
    
    def _extract_chapters_from_matches(self, text: str, matches: List) -> List[tuple]:
        """Extract chapter content based on regex matches"""
        chapters = []
        
        for i, match in enumerate(matches):
            title = match.group(1)
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            
            content = text[start:end]
            chapters.append((title, content))
        
        return chapters
    
    def _split_by_length(self, content: ProcessedContent, target_length: int = 2000) -> List[Chapter]:
        """Split content into chunks by length"""
        text = content.content
        chapters = []
        
        if len(text) <= target_length:
            return [Chapter(
                title=content.title or "Full Document",
                content=text,
                index=0
            )]
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        current_chunk = []
        current_length = 0
        chapter_index = 0
        
        for paragraph in paragraphs:
            if current_length + len(paragraph) > target_length and current_chunk:
                # Save current chunk
                chapters.append(Chapter(
                    title=f"Section {chapter_index + 1}",
                    content='\n\n'.join(current_chunk),
                    index=chapter_index
                ))
                
                current_chunk = [paragraph]
                current_length = len(paragraph)
                chapter_index += 1
            else:
                current_chunk.append(paragraph)
                current_length += len(paragraph)
        
        # Add remaining content
        if current_chunk:
            chapters.append(Chapter(
                title=f"Section {chapter_index + 1}",
                content='\n\n'.join(current_chunk),
                index=chapter_index
            ))
        
        return chapters
    
    def extract_topics(self, chapters: List[Chapter], max_topics: int = 20) -> List[str]:
        """Extract main topics from chapters for quiz/test generation"""
        topics = set()
        
        for chapter in chapters:
            # Extract sentences that might be important topics
            sentences = re.split(r'[.!?]+', chapter.content)
            
            for sentence in sentences:
                sentence = sentence.strip()
                if (20 <= len(sentence) <= 150 and 
                    not sentence.startswith(('The ', 'This ', 'It ', 'A ', 'An ')) and
                    len(sentence.split()) <= 15):
                    topics.add(sentence)
                
                if len(topics) >= max_topics:
                    break
            
            if len(topics) >= max_topics:
                break
        
        return list(topics)[:max_topics]


# Convenience functions
def process_file(file_path: str) -> ProcessedContent:
    """Process a file and return structured content"""
    processor = FileProcessor()
    return processor.process_file(file_path)


def organize_content(content: ProcessedContent) -> List[Chapter]:
    """Organize content into chapters"""
    organizer = ContentOrganizer()
    return organizer.organize_into_chapters(content)


def get_supported_extensions() -> List[str]:
    """Get list of supported file extensions"""
    return list(FileProcessor.SUPPORTED_EXTENSIONS.keys())


def check_dependencies() -> List[str]:
    """Check for missing dependencies"""
    processor = FileProcessor()
    return processor.get_missing_dependencies()
