"""
Debug OCR setup and test with sample image
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_ocr_setup():
    """Debug OCR setup"""
    print("🔍 Debugging OCR setup...")
    
    try:
        import pytesseract
        print("✅ pytesseract imported successfully")
        
        # Configure poppler path first
        import platform
        if platform.system() == "Windows":
            poppler_paths = [
                os.path.join(os.path.dirname(__file__), "poppler-21.11.0", "Library", "bin"),
                r"C:\poppler\poppler-21.11.0\Library\bin",
                r"C:\poppler\Library\bin",
                r"C:\Program Files\poppler\bin"
            ]
            for path in poppler_paths:
                if os.path.exists(path):
                    print(f"🔧 Found poppler at: {path}")
                    os.environ["PATH"] = path + ";" + os.environ.get("PATH", "")
                    print(f"🔧 Poppler configured in PATH")
                    break
        
        # Check Tesseract configuration
        print(f"📍 Tesseract command: {pytesseract.pytesseract.tesseract_cmd}")
        
        # Test basic Tesseract functionality
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract version: {version}")
        except Exception as e:
            print(f"❌ Tesseract version check failed: {e}")
            
            # Try to configure Tesseract path
            if platform.system() == "Windows":
                tesseract_paths = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                    r"C:\Users\Admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
                ]
                
                for path in tesseract_paths:
                    if os.path.exists(path):
                        print(f"🔧 Found Tesseract at: {path}")
                        pytesseract.pytesseract.tesseract_cmd = path
                        try:
                            version = pytesseract.get_tesseract_version()
                            print(f"✅ Tesseract configured successfully. Version: {version}")
                            break
                        except Exception as e2:
                            print(f"❌ Failed to configure Tesseract at {path}: {e2}")
                            continue
                else:
                    print("❌ Tesseract not found in standard locations")
                    return False
        
        # Test pdf2image
        try:
            from pdf2image import convert_from_path
            print("✅ pdf2image imported successfully")
            
            # Test with a single page
            pdf_path = "test_files/Vitamins and Minerals.pdf"
            if os.path.exists(pdf_path):
                print(f"📄 Testing PDF conversion: {pdf_path}")
                # Try with explicit poppler path
                poppler_path = os.path.join(os.path.dirname(__file__), "poppler-21.11.0", "Library", "bin")
                if os.path.exists(poppler_path):
                    print(f"🔧 Using poppler path: {poppler_path}")
                    images = convert_from_path(pdf_path, first_page=1, last_page=1, poppler_path=poppler_path)
                else:
                    images = convert_from_path(pdf_path, first_page=1, last_page=1)
                    
                if images:
                    print(f"✅ PDF converted to {len(images)} image(s)")
                    
                    # Test OCR on the first page
                    image = images[0]
                    text = pytesseract.image_to_string(image, lang='eng')
                    print(f"📝 OCR extracted {len(text)} characters")
                    print(f"🔤 Sample text: {text[:200]}...")
                    
                    return True
                else:
                    print("❌ No images extracted from PDF")
            else:
                print(f"❌ Test PDF not found: {pdf_path}")
                
        except Exception as e:
            print(f"❌ pdf2image test failed: {e}")
            import traceback
            traceback.print_exc()
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        
    return False

if __name__ == "__main__":
    success = debug_ocr_setup()
    if success:
        print("\n✅ OCR setup is working correctly!")
    else:
        print("\n❌ OCR setup needs attention")
        print("💡 Try installing Tesseract: https://github.com/tesseract-ocr/tesseract")
