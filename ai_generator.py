import google.generativeai as genai
import json
import asyncio
import re
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from key.env file
load_dotenv('key.env')

# Try to import mobile config for mobile compatibility
try:
    from mobile_config import mobile_config
    USE_MOBILE_CONFIG = True
except ImportError:
    USE_MOBILE_CONFIG = False

try:
    from config import GEMINI_API_KEY, DEFAULT_FLASHCARD_COUNT, DEFAULT_QUIZ_QUESTIONS, DEFAULT_TEST_QUESTIONS
except ImportError:
    GEMINI_API_KEY = ""
    DEFAULT_FLASHCARD_COUNT = 10
    DEFAULT_QUIZ_QUESTIONS = 5
    DEFAULT_TEST_QUESTIONS = 10

class AIStudyGenerator:
    """Handles AI-powered generation of study materials using Gemini API"""
    
    def __init__(self, api_key: str | None = None):
        """Initialize with Gemini API key"""
        # Priority order: parameter > mobile config > key.env file > config.py > environment variable
        if USE_MOBILE_CONFIG and mobile_config.has_api_key():
            self.api_key = mobile_config.get_api_key()
        else:
            self.api_key = (
                api_key or 
                os.getenv('GEMINI_API_KEY') or  # From key.env file (loaded by dotenv)
                GEMINI_API_KEY or               # From config.py
                os.environ.get('GEMINI_API_KEY') # From system environment
            )
        
        if self.api_key:
            os.environ["GOOGLE_API_KEY"] = self.api_key
            self.model = genai.GenerativeModel('gemini-2.5-flash') # type: ignore
            print("✅ Gemini AI configured successfully!")
        else:
            self.model = None
            print("Warning: No Gemini API key provided. Using mock data.")
            print("To use AI features:")
            print("1. Get a Gemini API key from https://makersuite.google.com/app/apikey")
            print("2. Add it to key.env file: GEMINI_API_KEY=your_key_here")
            print("3. Or set GEMINI_API_KEY environment variable")
            print("4. Or update config.py")
    
    async def generate_flashcards(self, chapter_content: str, max_cards: int = DEFAULT_FLASHCARD_COUNT) -> List[Dict[str, str]]:
        """Generate flashcards from chapter content"""
        if not self.model:
            return self._get_mock_flashcards()
        
        try:
            prompt = f"""
            Analyze the following text and create {max_cards} educational flashcards.
            
            Text: {chapter_content[:3000]}  # Limit text to avoid token limits
            
            Create flashcards that capture the most important concepts, terms, definitions, and key points.
            Return ONLY a valid JSON array in this exact format:
            [
                {{"term": "Key concept or term", "definition": "Clear, concise definition or explanation"}},
                {{"term": "Another concept", "definition": "Another clear explanation"}}
            ]
            
            Guidelines:
            - Focus on the most important and educational content
            - Keep definitions clear and concise
            - Include various types: definitions, concepts, facts, relationships
            - Make sure each flashcard tests understanding of a distinct concept
            """
            
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            
            # Extract JSON from response
            json_text = self._extract_json_from_response(response.text)
            flashcards = json.loads(json_text)
            
            # Validate format
            if isinstance(flashcards, list) and all(
                isinstance(card, dict) and 'term' in card and 'definition' in card 
                for card in flashcards
            ):
                return flashcards[:max_cards]
            else:
                raise ValueError("Invalid flashcard format received from AI")
                
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return self._get_mock_flashcards()
    
    async def generate_quiz(self, chapter_content: str, num_questions: int = DEFAULT_QUIZ_QUESTIONS) -> Dict[str, Any]:
        """Generate a multiple-choice quiz from chapter content"""
        if not self.model:
            return self._get_mock_quiz()
        
        try:
            prompt = f"""
            Create a {num_questions}-question multiple choice quiz based on the following text.
            
            Text: {chapter_content[:3000]}
            
            Return ONLY a valid JSON object in this exact format:
            {{
                "title": "Quiz Title",
                "questions": [
                    {{
                        "question": "Question text?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": 0,
                        "explanation": "Brief explanation of why this is correct"
                    }}
                ]
            }}
            
            Guidelines:
            - Questions should test comprehension, not just memorization
            - Include a mix of difficulty levels
            - Make incorrect options plausible but clearly wrong
            - Ensure correct_answer is the index (0-3) of the correct option
            - Keep explanations brief but helpful
            """
            
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            
            # Extract JSON from response
            json_text = self._extract_json_from_response(response.text)
            quiz_data = json.loads(json_text)
            
            # Validate format
            if self._validate_quiz_format(quiz_data):
                return quiz_data
            else:
                raise ValueError("Invalid quiz format received from AI")
                
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return self._get_mock_quiz()
    
    async def generate_test(self, chapter_content: str, num_questions: int = DEFAULT_TEST_QUESTIONS) -> Dict[str, Any]:
        """Generate a comprehensive test from chapter content"""
        if not self.model:
            return self._get_mock_test()
        
        try:
            prompt = f"""
            Create a comprehensive {num_questions}-question test based on the following text.
            Mix multiple choice and true/false questions.
            
            Text: {chapter_content[:3000]}
            
            Return ONLY a valid JSON object in this exact format:
            {{
                "title": "Test Title",
                "questions": [
                    {{
                        "question": "Question text?",
                        "type": "multiple_choice",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": 0,
                        "explanation": "Brief explanation"
                    }},
                    {{
                        "question": "True/false question?",
                        "type": "true_false",
                        "options": ["True", "False"],
                        "correct_answer": 0,
                        "explanation": "Brief explanation"
                    }}
                ]
            }}
            
            Guidelines:
            - Mix question types for variety
            - Test deep understanding, not just facts
            - Include challenging but fair questions
            - Ensure all questions are answerable from the text
            """
            
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            
            # Extract JSON from response
            json_text = self._extract_json_from_response(response.text)
            test_data = json.loads(json_text)
            
            # Validate format
            if self._validate_test_format(test_data):
                return test_data
            else:
                raise ValueError("Invalid test format received from AI")
                
        except Exception as e:
            print(f"Error generating test: {e}")
            return self._get_mock_test()
    
    def _extract_json_from_response(self, response_text: str) -> str:
        """Extract JSON from AI response, handling markdown formatting"""
        # Remove markdown code blocks
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        
        # Find JSON content between braces or brackets
        json_match = re.search(r'[\[\{].*[\]\}]', response_text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        return response_text.strip()
    
    def _validate_quiz_format(self, quiz_data: Dict) -> bool:
        """Validate quiz data format"""
        if not isinstance(quiz_data, dict) or 'questions' not in quiz_data:
            return False
        
        for question in quiz_data['questions']:
            if not all(key in question for key in ['question', 'options', 'correct_answer']):
                return False
            if not isinstance(question['options'], list) or len(question['options']) < 2:
                return False
            if not isinstance(question['correct_answer'], int):
                return False
            if question['correct_answer'] >= len(question['options']):
                return False
        
        return True
    
    def _validate_test_format(self, test_data: Dict) -> bool:
        """Validate test data format"""
        if not isinstance(test_data, dict) or 'questions' not in test_data:
            return False
        
        for question in test_data['questions']:
            if not all(key in question for key in ['question', 'type', 'options', 'correct_answer']):
                return False
            if question['type'] not in ['multiple_choice', 'true_false']:
                return False
            if not isinstance(question['options'], list):
                return False
            if not isinstance(question['correct_answer'], int):
                return False
            if question['correct_answer'] >= len(question['options']):
                return False
        
        return True
    
    def _get_mock_flashcards(self) -> List[Dict[str, str]]:
        """Fallback mock flashcards when API is unavailable"""
        return [
            {"term": "Study Method", "definition": "A systematic approach to learning and retaining information effectively."},
            {"term": "Active Recall", "definition": "A learning technique where you actively try to remember information without looking at the source."},
            {"term": "Spaced Repetition", "definition": "A learning technique that involves reviewing material at increasing intervals over time."},
            {"term": "Flashcard", "definition": "A card bearing information on both sides, used for drilling or self-testing."},
            {"term": "Cognitive Load", "definition": "The amount of mental effort being used in working memory during learning."},
        ]
    
    def _get_mock_quiz(self) -> Dict[str, Any]:
        """Fallback mock quiz when API is unavailable"""
        return {
            "title": "Sample Quiz",
            "questions": [
                {
                    "question": "What is the most effective way to study?",
                    "options": ["Reading repeatedly", "Active recall", "Highlighting", "Passive review"],
                    "correct_answer": 1,
                    "explanation": "Active recall forces your brain to retrieve information, strengthening memory pathways."
                },
                {
                    "question": "What is spaced repetition?",
                    "options": ["Studying the same topic repeatedly", "Reviewing material at increasing intervals", "Taking breaks while studying", "Studying multiple subjects at once"],
                    "correct_answer": 1,
                    "explanation": "Spaced repetition leverages the forgetting curve to optimize long-term retention."
                }
            ]
        }
    
    def _get_mock_test(self) -> Dict[str, Any]:
        """Fallback mock test when API is unavailable"""
        return {
            "title": "Comprehensive Test",
            "questions": [
                {
                    "question": "Flashcards are effective because they use active recall.",
                    "type": "true_false",
                    "options": ["True", "False"],
                    "correct_answer": 0,
                    "explanation": "True. Flashcards require you to actively retrieve information from memory."
                },
                {
                    "question": "Which of the following is NOT a principle of effective studying?",
                    "type": "multiple_choice",
                    "options": ["Spaced repetition", "Active recall", "Passive reading", "Self-testing"],
                    "correct_answer": 2,
                    "explanation": "Passive reading is less effective than active learning strategies."
                }
            ]
        }
    
    # Synchronous wrapper methods for mobile/desktop compatibility
    def generate_flashcards_sync(self, chapter_content: str, max_cards: int = None) -> List[Dict[str, str]]:
        """Synchronous wrapper for generate_flashcards"""
        if max_cards is None:
            max_cards = DEFAULT_FLASHCARD_COUNT
        return asyncio.run(self.generate_flashcards(chapter_content, max_cards))
    
    def generate_quiz_sync(self, chapter_content: str, num_questions: int = None) -> Dict[str, Any]:
        """Synchronous wrapper for generate_quiz"""
        if num_questions is None:
            num_questions = DEFAULT_QUIZ_QUESTIONS
        return asyncio.run(self.generate_quiz(chapter_content, num_questions))
    
    def generate_test_sync(self, chapter_content: str, num_questions: int = None) -> Dict[str, Any]:
        """Synchronous wrapper for generate_test"""
        if num_questions is None:
            num_questions = DEFAULT_TEST_QUESTIONS
        return asyncio.run(self.generate_test(chapter_content, num_questions))
    
    async def generate_summary(self, chapter_content: str) -> str:
        """Generate a summary of the study content"""
        if not self.api_key or not self.model:
            return self._get_mock_summary()
        
        prompt = f"""
        Please create a comprehensive summary of the following study material. 
        Make it concise but include all key points and main concepts.
        Format it with clear headings and bullet points where appropriate.
        
        Study Material:
        {chapter_content}
        
        Summary:
        """
        
        try:
            response = await self._generate_response(prompt)
            return response.strip()
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return self._get_mock_summary()
    
    def generate_summary_sync(self, chapter_content: str) -> str:
        """Synchronous wrapper for generate_summary"""
        return asyncio.run(self.generate_summary(chapter_content))
    
    def _get_mock_summary(self) -> str:
        """Fallback mock summary when API is unavailable"""
        return """
        # Study Material Summary
        
        ## Key Points
        • This content covers important study concepts
        • Active learning techniques are more effective than passive reading
        • Regular review and practice improve retention
        
        ## Main Topics
        • Study methods and techniques
        • Memory and retention strategies
        • Learning optimization
        
        ## Conclusion
        Effective studying requires active engagement with the material through techniques like active recall, spaced repetition, and self-testing.
        """
    
    async def _generate_response(self, prompt: str) -> str:
        """Helper method to generate response from the AI model"""
        response = await asyncio.to_thread(self.model.generate_content, prompt)
        return response.text
