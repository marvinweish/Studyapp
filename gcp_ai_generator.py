"""
GCP-compatible AI generator for Study Buddy
Handles cloud-specific configurations and optimizations
"""

import os
import logging
from typing import List, Dict, Any
import asyncio

# Try to import the base AI generator
try:
    from ai_generator import AIStudyGenerator as BaseAIGenerator
    print("✅ Using desktop AI generator")
except ImportError:
    print("⚠️ No AI generator found, using mock generator")
    BaseAIGenerator = None

logger = logging.getLogger(__name__)

class GCPAIGenerator:
    """GCP-optimized AI Study Generator"""
    
    def __init__(self):
        self.is_gcp = bool(
            os.environ.get('GAE_ENV') or
            os.environ.get('CLOUD_RUN_SERVICE') or
            os.environ.get('K_SERVICE') or
            os.environ.get('GOOGLE_CLOUD_PROJECT')
        )
        
        # Initialize base generator if available
        if BaseAIGenerator:
            try:
                self.base_generator = BaseAIGenerator()
                self.has_api = True
                logger.info("✅ AI generator initialized with API")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize AI generator: {e}")
                self.base_generator = None
                self.has_api = False
        else:
            self.base_generator = None
            self.has_api = False
            
        # Configure for GCP environment
        if self.is_gcp:
            logger.info("🌐 Running in GCP environment")
        else:
            logger.info("🖥️ Running in local environment")
    
    async def generate_flashcards(self, content: str, count: int = 10) -> List[Dict[str, str]]:
        """Generate flashcards from content"""
        if self.has_api and self.base_generator:
            try:
                return await self.base_generator.generate_flashcards(content, count)
            except Exception as e:
                logger.error(f"❌ API generation failed: {e}")
                return self._generate_mock_flashcards(content, count)
        else:
            return self._generate_mock_flashcards(content, count)
    
    async def generate_quiz(self, content: str, question_count: int = 5) -> Dict[str, Any]:
        """Generate quiz questions from content"""
        if self.has_api and self.base_generator:
            try:
                return await self.base_generator.generate_quiz(content, question_count)
            except Exception as e:
                logger.error(f"❌ API generation failed: {e}")
                return self._generate_mock_quiz(content, question_count)
        else:
            return self._generate_mock_quiz(content, question_count)
    
    async def generate_test(self, content: str, question_count: int = 10) -> Dict[str, Any]:
        """Generate test questions from content"""
        if self.has_api and self.base_generator:
            try:
                return await self.base_generator.generate_test(content, question_count)
            except Exception as e:
                logger.error(f"❌ API generation failed: {e}")
                return self._generate_mock_test(content, question_count)
        else:
            return self._generate_mock_test(content, question_count)
    
    def _generate_mock_flashcards(self, content: str, count: int) -> List[Dict[str, str]]:
        """Generate mock flashcards for testing/fallback"""
        words = content.split()[:count*2]  # Get enough words
        flashcards = []
        
        for i in range(min(count, len(words)//2)):
            flashcards.append({
                "term": f"Key Concept {i+1}",
                "definition": f"Important information from the content: {' '.join(words[i*2:(i+1)*2])}..."
            })
        
        # Ensure we have at least a few cards
        if len(flashcards) < 3:
            flashcards = [
                {"term": "Sample Term 1", "definition": "This is a sample definition for testing purposes."},
                {"term": "Sample Term 2", "definition": "Another sample definition to demonstrate the flashcard functionality."},
                {"term": "Sample Term 3", "definition": "A third sample to ensure the interface works properly."}
            ]
        
        return flashcards
    
    def _generate_mock_quiz(self, content: str, question_count: int) -> Dict[str, Any]:
        """Generate mock quiz for testing/fallback"""
        questions = []
        
        for i in range(question_count):
            questions.append({
                "question": f"Sample question {i+1} based on the content?",
                "options": [
                    f"Option A for question {i+1}",
                    f"Option B for question {i+1}",
                    f"Option C for question {i+1}",
                    f"Option D for question {i+1}"
                ],
                "correct_answer": i % 4,  # Rotate correct answers
                "explanation": f"This is the explanation for question {i+1}."
            })
        
        return {
            "title": "Sample Quiz",
            "questions": questions
        }
    
    def _generate_mock_test(self, content: str, question_count: int) -> Dict[str, Any]:
        """Generate mock test for testing/fallback"""
        questions = []
        
        for i in range(question_count):
            questions.append({
                "question": f"Test question {i+1}: What is the main concept discussed?",
                "options": [
                    f"Concept A related to question {i+1}",
                    f"Concept B related to question {i+1}",
                    f"Concept C related to question {i+1}",
                    f"Concept D related to question {i+1}"
                ],
                "correct_answer": (i + 1) % 4,  # Vary correct answers
                "type": "multiple_choice",
                "explanation": f"Detailed explanation for test question {i+1}. This explains why the correct answer is right and others are wrong."
            })
        
        return {
            "title": "Sample Test",
            "questions": questions
        }

# Create a singleton instance
ai_generator = GCPAIGenerator()
