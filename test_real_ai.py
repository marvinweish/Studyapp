#!/usr/bin/env python3
"""
Quick test of actual AI-powered flashcard generation
"""

import asyncio
from ai_generator import AIStudyGenerator

async def test_flashcard_generation():
    print("🧠 Testing Real AI Flashcard Generation...")
    print("-" * 50)
    
    # Sample text about Python programming
    sample_text = """
    Python is a high-level, interpreted programming language with dynamic semantics. 
    Its high-level built-in data structures, combined with dynamic typing and dynamic binding, 
    make it very attractive for Rapid Application Development. Python's simple, easy-to-learn 
    syntax emphasizes readability and therefore reduces the cost of program maintenance. 
    Python supports modules and packages, which encourages program modularity and code reuse.
    
    Variables in Python are created when you assign a value to them. Python has several 
    built-in data types including integers, floats, strings, and booleans. Lists are ordered 
    collections that can contain different data types. Dictionaries store key-value pairs 
    and provide fast lookup times.
    """
    
    ai_generator = AIStudyGenerator()
    
    if not ai_generator.model:
        print("❌ AI model not available")
        return False
    
    print("🔄 Generating flashcards from sample text...")
    try:
        flashcards = await ai_generator.generate_flashcards(sample_text, max_cards=3)
        
        print(f"✅ Generated {len(flashcards)} flashcards:")
        print("-" * 30)
        
        for i, card in enumerate(flashcards, 1):
            print(f"Card {i}:")
            print(f"  Term: {card['term']}")
            print(f"  Definition: {card['definition']}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating flashcards: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_flashcard_generation())
    if success:
        print("🎉 AI flashcard generation test successful!")
    else:
        print("❌ AI flashcard generation test failed!")
