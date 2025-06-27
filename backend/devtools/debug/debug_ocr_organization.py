"""
Debug the OCR organization method step by step
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_ocr_organization():
    """Debug the OCR organization method step by step"""
    print("🔍 Debugging OCR organization method...")
    
    # Read the OCR output
    if not os.path.exists("ocr_output.txt"):
        print("❌ OCR output file not found. Run test_direct_ocr.py first.")
        return
    
    with open("ocr_output.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
    
    print(f"📄 Raw OCR text: {len(raw_text)} characters")
    
    # Step 1: Create page texts
    page_texts = []
    pages = raw_text.split('\n\n')  # Simple split for testing
    for i, page_text in enumerate(pages[:5]):  # Test with first 5 pages only
        if page_text.strip():
            cleaned_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', page_text.strip())
            page_texts.append({
                'page': i + 1,
                'text': cleaned_text,
                'raw_text': page_text.strip()
            })
    
    print(f"📚 Using {len(page_texts)} text chunks for testing")
    
    # Step 2: Combine all text
    all_text = '\n\n'.join([page['text'] for page in page_texts])
    print(f"📝 Combined text: {len(all_text)} characters")
    print(f"🔤 Sample: {all_text[:300]}...")
    
    # Step 3: Split into sentences
    sentences = re.split(r'[.!?]+\s+', all_text)
    print(f"📝 Raw sentences: {len(sentences)}")
    
    # Step 4: Filter sentences
    cleaned_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if 10 <= len(sentence) <= 500 and len(sentence.split()) >= 3:
            cleaned_sentences.append(sentence)
    
    print(f"📝 Filtered sentences: {len(cleaned_sentences)}")
    if cleaned_sentences:
        print(f"🔤 First sentence: {cleaned_sentences[0]}")
        print(f"🔤 Last sentence: {cleaned_sentences[-1]}")
    
    # Step 5: Test keyword extraction
    def extract_keywords(text):
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'this', 'that', 'these', 'those', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'can', 'must', 'shall', 'from', 'up', 'out', 'off', 'over'
        }
        keywords = {word for word in words if word not in stop_words and len(word) > 3}
        return keywords
    
    if cleaned_sentences:
        sample_keywords = extract_keywords(cleaned_sentences[0])
        print(f"🔤 Sample keywords: {list(sample_keywords)[:10]}")
    
    # Step 6: Try simple topic grouping
    topic_groups = {}
    for i, sentence in enumerate(cleaned_sentences[:20]):  # Test with first 20 sentences
        keywords = extract_keywords(sentence)
        
        # Simple grouping - if no groups exist or no keyword overlap, create new group
        found_group = False
        for group_key, group_sentences in topic_groups.items():
            if group_sentences:
                first_sentence_keywords = extract_keywords(group_sentences[0])
                common = keywords.intersection(first_sentence_keywords)
                if common and len(common) >= 1:  # Lowered threshold for testing
                    topic_groups[group_key].append(sentence)
                    found_group = True
                    break
        
        if not found_group:
            topic_groups[f"topic_{len(topic_groups) + 1}"] = [sentence]
    
    print(f"📚 Topic groups created: {len(topic_groups)}")
    for group_key, group_sentences in topic_groups.items():
        print(f"   {group_key}: {len(group_sentences)} sentences")
    
    # Step 7: Generate sections
    organized_sections = []
    for i, (topic_key, topic_sentences) in enumerate(topic_groups.items()):
        if len(' '.join(topic_sentences)) > 50:  # Lowered threshold for testing
            section_title = f"Section {i + 1}"
            section_content = '. '.join(topic_sentences)
            organized_sections.append(f"{section_title}\n{'=' * len(section_title)}\n\n{section_content}")
    
    print(f"📊 Organized sections: {len(organized_sections)}")
    
    # Step 8: Final result
    final_text = '\n\n\n'.join(organized_sections)
    print(f"📄 Final organized text: {len(final_text)} characters")
    
    if final_text:
        print(f"🔤 Final sample: {final_text[:500]}...")
        
        with open("debug_organized.txt", "w", encoding="utf-8") as f:
            f.write(final_text)
        print("💾 Debug organized output saved to debug_organized.txt")
    
if __name__ == "__main__":
    debug_ocr_organization()
