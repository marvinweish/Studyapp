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
import platform
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
            os.path.join(os.path.dirname(__file__), "poppler-21.11.0", "Library", "bin"),
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

@dataclass
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
                            ocr_text = self._process_pdf_with_ocr(file_path)
                            if ocr_text.strip():
                                # Create a ProcessedContent object for the OCR text to use existing organizing functions
                                temp_content = ProcessedContent(
                                    title=metadata.get('title', Path(file_path).stem),
                                    content=ocr_text,
                                    file_type='pdf',
                                    metadata=metadata
                                )
                                # Return the organized content
                                return temp_content
                            else:
                                content = ["No readable text found in this PDF after OCR processing."]
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
    
    def _process_pdf_with_ocr(self, file_path: str) -> str:
        """Process PDF using OCR for image-based PDFs with intelligent content organization"""
        if not OCR_AVAILABLE:
            raise ImportError("OCR dependencies required. Install with: pip install pytesseract pdf2image pillow")
        
        try:
            # Convert PDF pages to images
            poppler_path = None
            if platform.system() == "Windows":
                # Try to find poppler in the project directory first
                project_poppler = os.path.join(os.path.dirname(__file__), "poppler-21.11.0", "Library", "bin")
                if os.path.exists(project_poppler):
                    poppler_path = project_poppler
            
            # Convert PDF with proper poppler path
            if poppler_path:
                images = convert_from_path(file_path, poppler_path=poppler_path)
            else:
                images = convert_from_path(file_path)
                
            page_texts = []
            
            for page_num, image in enumerate(images):
                try:
                    # Preprocess image to improve OCR accuracy
                    image = self._preprocess_image_for_ocr(image)
                    
                    # Use OCR to extract text from image with better configuration
                    custom_config = r'--oem 3 --psm 6'  # Better OCR settings
                    text = pytesseract.image_to_string(image, lang='eng', config=custom_config)
                    if text.strip():
                        cleaned_page_text = self._clean_ocr_text(text.strip())
                        page_texts.append({
                            'page': page_num + 1,
                            'text': cleaned_page_text,
                            'raw_text': text.strip()
                        })
                except Exception as e:
                    print(f"OCR error on page {page_num + 1}: {str(e)}")
                    continue
            
            # Intelligently combine pages into coherent content
            organized_text = self._organize_ocr_content(page_texts)
            
            return organized_text
        
        except Exception as e:
            raise ValueError(f"OCR processing failed: {str(e)}")
    
    def _preprocess_image_for_ocr(self, image):
        """Preprocess image to improve OCR accuracy"""
        try:
            from PIL import ImageEnhance, ImageFilter
            
            # Convert to grayscale if not already
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
            
            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.MedianFilter(size=1))
            
            return image
        except Exception as e:
            print(f"Image preprocessing failed: {e}")
            return image

    def _clean_ocr_text(self, text: str) -> str:
        """Clean OCR artifacts and improve text quality"""
        if not text.strip():
            return text
        
        # Remove excessive whitespace and normalize line breaks
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple empty lines to double
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
        
        # Fix common OCR character recognition errors
        ocr_fixes = {
            r'\b0\b': 'O',  # Zero to O when it's likely a letter
            r'\bl\b': 'I',  # lowercase l to I when standalone
            r'\brn\b': 'm',  # common rn/m confusion
            r'\b1\b(?=[a-zA-Z])': 'l',  # 1 to l when followed by letters
            r'(?<=[a-zA-Z])\b1\b': 'l',  # 1 to l when preceded by letters
            r'\bvv\b': 'w',  # double v to w
            r'\|\|': 'll',  # pipe characters to ll
            r'["""]': '"',  # Normalize quotes
            r"[''']": "'",  # Normalize apostrophes
            r'—': '-',  # Em dash to hyphen
            r'–': '-',  # En dash to hyphen
        }
        
        for pattern, replacement in ocr_fixes.items():
            text = re.sub(pattern, replacement, text)
        
        # Remove standalone special characters that are likely OCR errors
        text = re.sub(r'\n[^\w\s]{1,3}\n', '\n', text)
        
        # Fix broken words (letters separated by spaces)
        text = re.sub(r'\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b', r'\1\2\3', text)
        
        # Remove page numbers and headers/footers (common patterns)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)  # Standalone page numbers
        text = re.sub(r'\n\s*Page\s+\d+\s*\n', '\n', text, re.IGNORECASE)
        
        # Remove short lines that are likely artifacts (less than 3 characters)
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if len(line) >= 3 or line == '':  # Keep empty lines for paragraph breaks
                cleaned_lines.append(line)
        
        text = '\n'.join(cleaned_lines)
        
        # Final cleanup - normalize paragraph breaks
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = text.strip()
        
        return text
    
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
                    if paragraph.style and paragraph.style.name and paragraph.style.name.startswith('Heading'):
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
                    try:
                        # Use getattr to safely access text properties
                        text = None
                        
                        # Try text_frame.text first (most common for text boxes)
                        text_frame = getattr(shape, 'text_frame', None)
                        if text_frame:
                            text = getattr(text_frame, 'text', None)
                        
                        # Fall back to direct text attribute
                        if not text:
                            text = getattr(shape, 'text', None)
                        
                        if text and text.strip():
                            slide_content.append(text.strip())
                    except Exception:
                        # Skip shapes that cause any errors
                        continue
                
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
    
    def _organize_ocr_content(self, page_texts: List[Dict]) -> str:
        """Intelligently organize OCR content from multiple pages into coherent sections"""
        if not page_texts:
            return ""
        
        # Combine all text first with clear page separators
        all_text = '\n\n'.join([page['text'] for page in page_texts])
        
        # For now, use a simpler approach - split into topic-based sections
        # by looking for clear topic breaks and organize accordingly
        sections = self._create_topic_sections(all_text)
        
        if sections:
            return '\n\n\n'.join(sections)
        else:
            # Fallback: return the cleaned combined text with basic organization
            return self._basic_organize_text(all_text)
    
    def _create_topic_sections(self, text: str) -> List[str]:
        """Create topic-based sections from OCR text"""
        sections = []
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return []
        
        # Group paragraphs into logical sections
        current_section = []
        current_topic = None
        
        for paragraph in paragraphs:
            # Skip very short paragraphs (likely artifacts)
            if len(paragraph) < 20:
                continue
            
            # Check if this looks like a new topic/section header
            if self._is_topic_header(paragraph):
                # Save previous section if it exists
                if current_section:
                    section_content = '\n\n'.join(current_section)
                    if len(section_content) > 100:  # Only include substantial sections
                        title = current_topic or f"Section {len(sections) + 1}"
                        sections.append(f"{title}\n{'=' * len(title)}\n\n{section_content}")
                
                # Start new section
                current_topic = self._extract_topic_title(paragraph)
                current_section = [paragraph]
            else:
                # Add to current section
                current_section.append(paragraph)
        
        # Add final section
        if current_section:
            section_content = '\n\n'.join(current_section)
            if len(section_content) > 100:
                title = current_topic or f"Section {len(sections) + 1}"
                sections.append(f"{title}\n{'=' * len(title)}\n\n{section_content}")
        
        return sections
    
    def _is_topic_header(self, paragraph: str) -> bool:
        """Check if a paragraph looks like a topic header"""
        # Skip common headers/footers
        if any(skip in paragraph.lower() for skip in [
            'better health channel', 'betterhealth', 'pm vitamins', 'http://', 'www.'
        ]):
            return False
        
        # Look for topic indicators
        lines = paragraph.split('\n')
        if lines:
            first_line = lines[0].strip()
            
            # Check for topic indicators
            if (len(first_line) < 50 and  # Short enough to be a header
                len(first_line) > 5 and   # Long enough to be meaningful
                not first_line.endswith('.') and  # Doesn't end with period
                not first_line.startswith('e ') and  # Not a bullet point
                any(word.lower() in first_line.lower() for word in [
                    'vitamin', 'mineral', 'calcium', 'iron', 'zinc', 'potassium', 
                    'sodium', 'deficiency', 'dietary', 'sources', 'food'
                ])):
                return True
        
        return False
    
    def _extract_topic_title(self, paragraph: str) -> str:
        """Extract a clean topic title from a paragraph"""
        lines = paragraph.split('\n')
        if lines:
            first_line = lines[0].strip()
            
            # Clean up common artifacts
            first_line = re.sub(r'^[°•\-\s]+', '', first_line)  # Remove bullet points
            first_line = re.sub(r'\s+', ' ', first_line)        # Normalize spaces
            
            # Capitalize properly
            if first_line and len(first_line) < 80:
                return first_line.title()
        
        return "Topic Section"
    
    def _basic_organize_text(self, text: str) -> str:
        """Basic text organization as fallback"""
        # Split into paragraphs and group by estimated topic changes
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 20]
        
        if not paragraphs:
            return text
        
        # Group paragraphs into sections of reasonable length
        sections = []
        current_section = []
        current_length = 0
        target_length = 1500  # Target characters per section
        
        for paragraph in paragraphs:
            # Skip headers/footers
            if any(skip in paragraph.lower() for skip in [
                'better health channel', 'betterhealth', 'pm vitamins'
            ]):
                continue
            
            if current_length + len(paragraph) > target_length and current_section:
                # Save current section
                section_content = '\n\n'.join(current_section)
                title = f"Section {len(sections) + 1}"
                sections.append(f"{title}\n{'=' * len(title)}\n\n{section_content}")
                
                current_section = [paragraph]
                current_length = len(paragraph)
            else:
                current_section.append(paragraph)
                current_length += len(paragraph)
        
        # Add final section
        if current_section:
            section_content = '\n\n'.join(current_section)
            title = f"Section {len(sections) + 1}"
            sections.append(f"{title}\n{'=' * len(title)}\n\n{section_content}")
        
        return '\n\n\n'.join(sections)
    
    # Legacy methods - keeping for reference but not used in new implementation
    # def _split_into_sentences(self, text: str) -> List[str]:
    # def _group_sentences_by_topic(self, sentences: List[str]) -> Dict[str, List[str]]:
    # def _extract_keywords(self, text: str) -> set:
    # def _generate_section_title(self, sentences: List[str], section_num: int) -> str:
    

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
        """Organize content into chapters based on patterns or intelligent content analysis"""
        text = content.content
        chapters = []
        
        # Check if this is likely OCR content (contains section headers with '=' markers)
        if self._is_ocr_organized_content(text):
            return self._organize_ocr_chapters(content)
        
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
            # If no chapters found, use intelligent content splitting
            chapters = self._split_by_length(content, min_chapter_length)
        
        return chapters
    
    def _is_ocr_organized_content(self, text: str) -> bool:
        """Check if content appears to be organized by OCR processing (has section headers with '=' markers)"""
        return bool(re.search(r'\n[A-Za-z][^=\n]*\n=+\n', text))
    
    def _organize_ocr_chapters(self, content: ProcessedContent) -> List[Chapter]:
        """Organize content that was already structured by OCR processing"""
        text = content.content
        chapters = []
        
        # Split by section headers (lines followed by equals signs)
        sections = re.split(r'\n([A-Za-z][^=\n]*)\n=+\n', text)
        
        if len(sections) > 1:
            # First section might be introduction or summary
            if sections[0].strip():
                chapters.append(Chapter(
                    title="Introduction",
                    content=sections[0].strip(),
                    index=0
                ))
            
            # Process remaining sections
            for i in range(1, len(sections), 2):
                if i + 1 < len(sections):
                    title = sections[i].strip()
                    section_content = sections[i + 1].strip()
                    
                    if section_content and len(section_content) > 100:  # Minimum content length
                        chapters.append(Chapter(
                            title=title,
                            content=section_content,
                            index=len(chapters)
                        ))
        else:
            # Fallback to length-based splitting
            chapters = self._split_by_length(content, 500)
        
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
            title = match.group(1).strip()
            start_pos = match.end()
            
            # Find the end position (start of next chapter or end of text)
            if i + 1 < len(matches):
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(text)
            
            content = text[start_pos:end_pos].strip()
            if content:
                chapters.append((title, content))
        
        return chapters
        
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
