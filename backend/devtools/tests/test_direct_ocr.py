"""
Direct OCR test to understand the issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_direct_ocr():
    """Test OCR processing directly"""
    print("🔍 Testing direct OCR processing...")
    
    try:
        # Import required modules
        import pytesseract
        from pdf2image import convert_from_path
        import platform
        
        # Configure Tesseract path
        if platform.system() == "Windows":
            tesseract_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                r"C:\Users\Admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
            ]
            
            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
        
        pdf_path = "test_files/Vitamins and Minerals.pdf"
        print(f"📄 Processing: {pdf_path}")
        
        # Convert PDF to images
        poppler_path = os.path.join(os.path.dirname(__file__), "poppler-21.11.0", "Library", "bin")
        print(f"🔧 Using poppler path: {poppler_path}")
        
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        print(f"✅ Converted to {len(images)} image(s)")
        
        # Process each page
        all_text = []
        for page_num, image in enumerate(images):
            print(f"📄 Processing page {page_num + 1}...")
            
            # Extract text
            text = pytesseract.image_to_string(image, lang='eng')
            print(f"   📝 Extracted {len(text)} characters")
            print(f"   🔤 Sample: {text[:200]}...")
            
            if text.strip():
                all_text.append(text.strip())
        
        # Combine all text
        combined_text = '\n\n'.join(all_text)
        print(f"\n📊 Total combined text: {len(combined_text)} characters")
        print(f"🔤 Combined sample: {combined_text[:500]}...")
        
        # Save to file for inspection
        with open("ocr_output.txt", "w", encoding="utf-8") as f:
            f.write(combined_text)
        print(f"💾 Full OCR output saved to ocr_output.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_ocr()
