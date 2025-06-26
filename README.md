# AI Study Buddy

A Python application built with Flet that helps you study by converting text documents into interactive flashcards.

## Features

- Upload text files (.txt)
- Automatically parse chapters from books
- Generate flashcards from chapter content
- Interactive flashcard study interface
- Dark theme UI

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python study_app.py
```

## Usage

1. Click the upload button in the app bar to upload a .txt file
2. Select a chapter you want to study
3. Choose "Flashcards" as your study method
4. Use the navigation buttons to go through flashcards
5. Click "Flip Card" or click on the card itself to see the definition

## Dependencies

- flet: Cross-platform app framework for Python
