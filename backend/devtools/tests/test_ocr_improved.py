"""
Test script for improved OCR processing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from file_processor import process_file, organize_content

def test_improved_ocr():
    """Test the improved OCR processing with the Vitamins and Minerals PDF"""
    pdf_path = "test_files/Vitamins and Minerals.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ Test file not found: {pdf_path}")
        return
    
    try:
        print("🔍 Processing PDF with improved OCR...")
        
        # Process the file
        processed_content = process_file(pdf_path)
        print(f"✅ File processed successfully")
        print(f"📄 Content length: {len(processed_content.content)} characters")
        
        # Organize into chapters
        chapters = organize_content(processed_content)
        print(f"📚 Organized into {len(chapters)} chapters/sections")
        
        # Display chapter information
        for i, chapter in enumerate(chapters):
            print(f"\n📖 Chapter {i+1}: {chapter.title}")
            print(f"   Length: {len(chapter.content)} characters")
            print(f"   Preview: {chapter.content[:200]}...")
            
        print(f"\n✅ Test completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Total chapters: {len(chapters)}")
        print(f"   - Average chapter length: {sum(len(c.content) for c in chapters) // len(chapters) if chapters else 0} characters")
        
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_ocr()
