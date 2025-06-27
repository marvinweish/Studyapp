"""
Test the OCR organization logic specifically
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ocr_organization():
    """Test the OCR content organization logic"""
    print("🔍 Testing OCR content organization...")
    
    # Read the OCR output we saved
    if not os.path.exists("ocr_output.txt"):
        print("❌ OCR output file not found. Run test_direct_ocr.py first.")
        return
    
    with open("ocr_output.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
    
    print(f"📄 Raw OCR text: {len(raw_text)} characters")
    
    # Import the FileProcessor to test the organization method
    from file_processor import FileProcessor
    
    processor = FileProcessor()
    
    # Create mock page texts like the OCR method would
    page_texts = []
    pages = raw_text.split('\n\n')  # Simple split for testing
    for i, page_text in enumerate(pages):
        if page_text.strip():
            page_texts.append({
                'page': i + 1,
                'text': page_text.strip(),
                'raw_text': page_text.strip()
            })
    
    print(f"📚 Split into {len(page_texts)} text chunks")
    
    try:
        # Test the organization method
        organized_text = processor._organize_ocr_content(page_texts)
        print(f"📊 Organized text: {len(organized_text)} characters")
        print(f"🔤 Organized sample: {organized_text[:500]}...")
        
        if len(organized_text) > 100:
            print("✅ OCR organization successful!")
            
            # Save organized output
            with open("organized_output.txt", "w", encoding="utf-8") as f:
                f.write(organized_text)
            print("💾 Organized output saved to organized_output.txt")
        else:
            print("❌ OCR organization failed or produced minimal content")
            
    except Exception as e:
        print(f"❌ Error in organization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ocr_organization()
