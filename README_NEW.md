# AI Study Buddy - Smart Learning Application

A modern study application built with Python and Flet that transforms your documents into interactive learning experiences using AI-powered flashcards, quizzes, and tests.

## 🚀 Features

### Core Functionality
- **Multi-format Document Support**: Upload TXT, PDF, DOCX, PPTX, and EPUB files
- **Automatic Chapter Detection**: Intelligently segments documents into study chapters
- **AI-Powered Study Materials**: Generate flashcards, quizzes, and tests using Google's Gemini AI

### Study Modes
1. **Flashcards** 📚
   - AI-generated term/definition pairs
   - Interactive flip-card interface
   - Progress tracking
   - Navigate between cards

2. **Quiz Mode** 🎯
   - Multiple-choice questions
   - Immediate feedback
   - Score calculation and results
   - Retry functionality

3. **Test Mode** 📝
   - Comprehensive assessments
   - Mixed question types (Multiple choice, True/False)
   - Detailed results with explanations
   - Grade calculation (A-F scale)
   - Question-by-question breakdown

### User Interface
- Modern, dark-themed design
- Cross-platform compatibility (Windows, macOS, Linux, Web)
- Intuitive navigation with back button support
- Loading indicators for better UX
- Responsive layout with scrollable content

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection (for AI features)

### Setup
1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Gemini API (for AI features):
   - Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set environment variable: `GEMINI_API_KEY=your_api_key_here`
   - Or edit `config.py` and add your API key

4. Run the application:
   ```bash
   python study_app.py
   ```

## 📖 Usage

1. **Upload a Document**: Click the upload button in the top-right corner
2. **Select a Chapter**: Choose from the automatically detected chapters
3. **Pick Study Mode**: Select Flashcards, Quiz, or Test
4. **Study & Learn**: Interact with AI-generated content
5. **Review Results**: Check your progress and understanding

## 🧠 AI Integration

The app uses Google's Gemini AI to:
- Extract key concepts and terms from your documents
- Generate educational flashcards with clear definitions
- Create challenging quiz questions with multiple-choice answers
- Design comprehensive tests with explanations
- Ensure content relevance and educational value

### Fallback Mode
If no API key is configured, the app uses high-quality mock data for demonstration purposes.

## 📁 Supported File Formats

- **TXT**: Plain text files
- **PDF**: Portable Document Format
- **DOCX**: Microsoft Word documents
- **PPTX**: Microsoft PowerPoint presentations
- **EPUB**: Electronic publication format

## 🔧 Configuration

Edit `config.py` to customize:
- Default number of flashcards (default: 10)
- Quiz question count (default: 5)
- Test question count (default: 10)
- API key settings

## 🎯 Educational Benefits

- **Active Recall**: Flashcards promote memory retrieval
- **Spaced Repetition**: Review materials at your own pace
- **Self-Assessment**: Quizzes and tests measure understanding
- **Immediate Feedback**: Learn from mistakes instantly
- **Progress Tracking**: Monitor your learning journey

## 🏗️ Technical Architecture

- **Frontend**: Flet (Flutter for Python)
- **AI Integration**: Google Generative AI (Gemini)
- **File Processing**: Custom processors for each format
- **State Management**: Centralized app state handling
- **Async Operations**: Non-blocking UI for better performance

## 🤝 Contributing

Feel free to contribute by:
- Adding new file format support
- Improving AI prompts
- Enhancing UI/UX
- Adding new study modes
- Optimizing performance

## 📄 License

This project is open-source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues
1. **File not supported**: Check if all dependencies are installed
2. **AI features not working**: Verify your Gemini API key
3. **Slow processing**: Large files may take time to process

### Getting Help
- Check the console for error messages
- Ensure all dependencies are properly installed
- Verify your internet connection for AI features

---

**Happy Learning! 🎓**
