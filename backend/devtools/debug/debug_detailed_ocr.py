"""
Debug detailed OCR processing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_detailed_ocr():
    """Debug the detailed OCR processing flow"""
    print("🔍 Debugging detailed OCR processing...")
    
    # Import the file processor and test directly
    from file_processor import FileProcessor
    
    processor = FileProcessor()
    pdf_path = "test_files/Vitamins and Minerals.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ Test file not found: {pdf_path}")
        return
    
    try:
        print("📄 Processing PDF with FileProcessor...")
        
        # Process the file directly
        processed_content = processor.process_file(pdf_path)
        print(f"✅ Processing completed")
        print(f"📋 Title: {processed_content.title}")
        print(f"📄 File type: {processed_content.file_type}")
        print(f"📝 Content length: {len(processed_content.content)} characters")
        print(f"🔤 Content preview: {processed_content.content[:500]}...")
        
        if len(processed_content.content) > 100:
            print("✅ OCR extraction successful!")
        else:
            print("❌ OCR extraction failed or produced minimal content")
            
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_detailed_ocr()
