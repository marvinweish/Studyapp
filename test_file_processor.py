"""
Test script for the File Processor module

This script demonstrates the capabilities of the file processor
and can be used to test different file formats.
"""

from file_processor import FileProcessor, ContentOrganizer, check_dependencies
import sys
import os

def test_file_processor():
    """Test the file processor with different scenarios"""
    print("=== AI Study Buddy File Processor Test ===\n")
    
    # Check dependencies
    print("1. Checking dependencies...")
    missing_deps = check_dependencies()
    if missing_deps:
        print(f"⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print(f"Install with: pip install {' '.join(missing_deps)}")
    else:
        print("✅ All dependencies are installed!")
    
    print()
    
    # Initialize processor and organizer
    processor = FileProcessor()
    organizer = ContentOrganizer()
    
    print("2. Supported file formats:")
    for ext, file_type in processor.SUPPORTED_EXTENSIONS.items():
        print(f"   {ext} -> {file_type}")
    
    print()
    
    # Test with files
    if len(sys.argv) > 1:
        # Single file provided
        file_path = sys.argv[1]
        print(f"3. Testing with file: {file_path}")
        test_single_file(processor, organizer, file_path)
    else:
        # Test all files in test_files directory
        test_files_dir = "test_files"
        if os.path.exists(test_files_dir):
            print(f"3. Testing all files in {test_files_dir}/ directory:")
            test_files = [f for f in os.listdir(test_files_dir) if os.path.isfile(os.path.join(test_files_dir, f))]
            
            if test_files:
                for i, filename in enumerate(test_files, 1):
                    file_path = os.path.join(test_files_dir, filename)
                    print(f"\n--- Test {i}/{len(test_files)}: {filename} ---")
                    test_single_file(processor, organizer, file_path)
            else:
                print("   No files found in test_files directory")
        else:
            print(f"3. No test files directory found. Usage: python test_file_processor.py <file_path>")

def test_single_file(processor, organizer, file_path):
    """Test processing of a single file"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    try:
        # Process the file
        print("   Processing file...")
        processed_content = processor.process_file(file_path)
        
        print(f"   ✅ Successfully processed {processed_content.file_type.upper()} file")
        print(f"   Title: {processed_content.title}")
        print(f"   Content length: {len(processed_content.content)} characters")
        
        if processed_content.metadata:
            print(f"   Metadata: {processed_content.metadata}")
        
        # Organize into chapters
        print("   Organizing into chapters...")
        chapters = organizer.organize_into_chapters(processed_content)
        
        print(f"   ✅ Organized into {len(chapters)} chapters:")
        for i, chapter in enumerate(chapters):
            print(f"      {i+1}. {chapter.title} ({len(chapter.content)} chars)")
        
        # Extract topics
        print("   Extracting topics...")
        topics = organizer.extract_topics(chapters)
        print(f"   ✅ Extracted {len(topics)} topics:")
        for topic in topics[:3]:  # Show first 3
            print(f"      - {topic[:60]}...")
        if len(topics) > 3:
            print(f"      ... and {len(topics) - 3} more")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_file_processor()
