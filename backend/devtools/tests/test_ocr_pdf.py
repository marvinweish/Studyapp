#!/usr/bin/env python3
"""
Test script to check OCR PDF processing capability
"""

import os
import sys
from file_processor import FileProcessor, ContentOrganizer

def test_pdf_processing():
    """Test PDF processing with the Vitamins and Minerals PDF"""
    pdf_path = "test_files/Vitamins and Minerals.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return False
    
    print("Testing PDF processing with OCR support...")
    print(f"File: {pdf_path}")
    print("-" * 50)
    
    try:
        # Create processor and organizer
        processor = FileProcessor()
        organizer = ContentOrganizer()
        
        # Check dependencies
        missing_deps = processor.get_missing_dependencies()
        if missing_deps:
            print(f"⚠️  Missing dependencies: {', '.join(missing_deps)}")
        else:
            print("✅ All dependencies available")
        
        # Process the PDF
        print("\nProcessing PDF...")
        processed_content = processor.process_file(pdf_path)
        
        print(f"Title: {processed_content.title}")
        print(f"File type: {processed_content.file_type}")
        print(f"Content length: {len(processed_content.content)} characters")
        
        # Show first 500 characters of content
        print(f"\nFirst 500 characters of extracted content:")
        print("-" * 50)
        print(processed_content.content[:500])
        print("..." if len(processed_content.content) > 500 else "")
        
        # Organize into chapters
        print("\nOrganizing content into chapters...")
        chapters = organizer.organize_into_chapters(processed_content)
        
        print(f"Generated {len(chapters)} chapters:")
        for i, chapter in enumerate(chapters):
            print(f"  Chapter {i+1}: {chapter.title} ({len(chapter.content)} chars)")
        
        # Show first chapter content sample
        if chapters:
            print(f"\nSample from first chapter:")
            print("-" * 30)
            print(chapters[0].content[:200])
            print("..." if len(chapters[0].content) > 200 else "")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_processing()
    sys.exit(0 if success else 1)
