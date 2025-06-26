import flet as ft
import re
import asyncio
import json
import os
from file_processor import FileProcessor, ContentOrganizer, get_supported_extensions, check_dependencies
from ai_generator import AIStudyGenerator

# A simple class to hold the state of our application
class AppState:
    def __init__(self):
        self.chapters = []
        self.current_flashcards = []
        self.current_flashcard_index = 0
        self.current_quiz = None
        self.current_test = None
        self.quiz_answers = []
        self.test_answers = []
        self.quiz_score = 0
        self.test_score = 0
        self.current_chapter_index = None  # Track current chapter
        self.saved_topics = []  # Store previously uploaded topics
        self.current_topic_title = ""  # Current topic title
        self.topics_file = "saved_topics.json"  # File to persist topics

    def set_chapters(self, chapters):
        self.chapters = chapters

    def set_current_chapter(self, chapter_index):
        """Set the current chapter index for navigation"""
        self.current_chapter_index = chapter_index

    def load_saved_topics(self):
        """Load previously saved topics from file"""
        try:
            if os.path.exists(self.topics_file):
                with open(self.topics_file, 'r', encoding='utf-8') as f:
                    self.saved_topics = json.load(f)
        except Exception as e:
            print(f"Error loading saved topics: {e}")
            self.saved_topics = []

    def save_topic(self, title, chapters):
        """Save a topic with its chapters"""
        try:
            # Check if topic already exists and update it
            for i, topic in enumerate(self.saved_topics):
                if topic['title'] == title:
                    self.saved_topics[i] = {'title': title, 'chapters': chapters}
                    break
            else:
                # Add new topic
                self.saved_topics.append({'title': title, 'chapters': chapters})
            
            # Save to file
            with open(self.topics_file, 'w', encoding='utf-8') as f:
                json.dump(self.saved_topics, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving topic: {e}")

    def load_topic(self, topic_title):
        """Load a previously saved topic"""
        for topic in self.saved_topics:
            if topic['title'] == topic_title:
                self.chapters = topic['chapters']
                self.current_topic_title = topic_title
                return True
        return False

    def delete_topic(self, topic_title):
        """Delete a saved topic"""
        try:
            self.saved_topics = [t for t in self.saved_topics if t['title'] != topic_title]
            with open(self.topics_file, 'w', encoding='utf-8') as f:
                json.dump(self.saved_topics, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error deleting topic: {e}")
            return False

    def set_flashcards(self, flashcards):
        self.current_flashcards = flashcards
        self.current_flashcard_index = 0

    def set_quiz(self, quiz_data):
        self.current_quiz = quiz_data
        self.quiz_answers = [None] * len(quiz_data['questions'])
        self.quiz_score = 0

    def set_test(self, test_data):
        self.current_test = test_data
        self.test_answers = [None] * len(test_data['questions'])
        self.test_score = 0

    def get_current_flashcard(self):
        if self.current_flashcards and 0 <= self.current_flashcard_index < len(self.current_flashcards):
            return self.current_flashcards[self.current_flashcard_index]
        return None

    def next_flashcard(self):
        if self.current_flashcard_index < len(self.current_flashcards) - 1:
            self.current_flashcard_index += 1
            return True
        return False

    def prev_flashcard(self):
        if self.current_flashcard_index > 0:
            self.current_flashcard_index -= 1
            return True
        return False

app_state = AppState()
ai_generator = AIStudyGenerator()  # Initialize AI generator

def main(page: ft.Page):
    page.title = "AI Study Buddy"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.all(20)

    # Load saved topics on startup
    app_state.load_saved_topics()

    # --- Loading Screen ---
    loading_screen = ft.Column(
        controls=[
            ft.Container(height=100),  # Spacer
            ft.Icon(ft.Icons.SCHOOL, size=120, color=ft.Colors.BLUE),
            ft.Text("AI Study Buddy", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
            ft.Text("Your intelligent learning companion", size=16, color=ft.Colors.BLUE_GREY),
            ft.Container(height=50),  # Spacer
            ft.ProgressRing(width=40, height=40, color=ft.Colors.BLUE),
            ft.Text("Loading...", size=14, color=ft.Colors.BLUE_GREY),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        visible=True,
    )

    # --- Helper Functions ---
    def show_loading(show: bool):
        """Shows or hides a loading indicator."""
        loading_indicator.visible = show
        page.update()

    def show_snack_bar(message: str, color):
        """Helper function to show snack bar messages"""
        snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    async def generate_flashcards_from_text(chapter_content: str):
        """Uses the Gemini API to generate flashcards from text."""
        show_loading(True)
        try:
            flashcards = await ai_generator.generate_flashcards(chapter_content)
            show_loading(False)
            return flashcards
        except Exception as e:
            show_loading(False)
            print(f"Error generating flashcards: {e}")
            return []

    # --- UI Views ---
    main_view_content = ft.Column(
        controls=[],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
        visible=False,
    )

    # View for study options (Flashcards, Quiz, etc.)
    study_options_view = ft.Column(
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )

    # View for flashcard interaction
    flashcard_view = ft.Column(
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )

    # View for quiz interaction
    quiz_view = ft.Column(
        visible=False,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )

    # View for test interaction
    test_view = ft.Column(
        visible=False,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )

    # --- Topic Management Functions ---
    def load_saved_topic(topic_title: str):
        """Load a previously saved topic"""
        if app_state.load_topic(topic_title):
            build_chapter_list_view()
            show_snack_bar(f"Loaded topic: {topic_title}", ft.Colors.GREEN_400)
        else:
            show_snack_bar(f"Failed to load topic: {topic_title}", ft.Colors.RED_400)

    def delete_saved_topic(topic_title: str):
        """Delete a saved topic with confirmation"""
        def confirm_delete(e):
            if app_state.delete_topic(topic_title):
                build_chapter_list_view()
                show_snack_bar(f"Deleted topic: {topic_title}", ft.Colors.GREEN_400)
            else:
                show_snack_bar(f"Failed to delete topic: {topic_title}", ft.Colors.RED_400)
            page.close(dialog)

        def cancel_delete(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete '{topic_title}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.TextButton("Delete", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
        )
        page.open(dialog)

    def save_current_topic():
        """Save or update the current topic"""
        if not app_state.chapters:
            show_snack_bar("No chapters to save", ft.Colors.RED_400)
            return

        def save_with_title(title: str):
            if title.strip():
                app_state.save_topic(title.strip(), app_state.chapters)
                app_state.current_topic_title = title.strip()
                build_chapter_list_view()
                show_snack_bar(f"Saved topic: {title.strip()}", ft.Colors.GREEN_400)

        if app_state.current_topic_title:
            # Update existing topic
            save_with_title(app_state.current_topic_title)
        else:
            # Prompt for new topic name
            title_field = ft.TextField(label="Topic Title", width=300)

            def confirm_save(e):
                if title_field.value:
                    save_with_title(title_field.value)
                page.close(dialog)

            def cancel_save(e):
                page.close(dialog)

            dialog = ft.AlertDialog(
                title=ft.Text("Save Topic"),
                content=ft.Column([
                    ft.Text("Enter a title for this topic:"),
                    title_field
                ], tight=True),
                actions=[
                    ft.TextButton("Cancel", on_click=cancel_save),
                    ft.TextButton("Save", on_click=confirm_save),
                ],
            )
            page.open(dialog)

    # --- Main View Builder ---
    def build_chapter_list_view():
        """Creates the list of chapters after a book is loaded."""
        main_view_content.controls.clear()
        
        # Add saved topics section if available
        if app_state.saved_topics:
            main_view_content.controls.append(ft.Text("📚 Saved Topics:", size=20, weight=ft.FontWeight.BOLD))
            
            saved_topics_row = ft.Row(wrap=True, spacing=10)
            for topic in app_state.saved_topics:
                topic_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(topic['title'], size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                            ft.Text(f"{len(topic['chapters'])} chapters", size=12, color=ft.Colors.BLUE_GREY),
                            ft.Row([
                                ft.IconButton(
                                    ft.Icons.PLAY_ARROW, 
                                    tooltip="Load Topic",
                                    on_click=lambda e, title=topic['title']: load_saved_topic(title),
                                    icon_size=16
                                ),
                                ft.IconButton(
                                    ft.Icons.DELETE, 
                                    tooltip="Delete Topic",
                                    on_click=lambda e, title=topic['title']: delete_saved_topic(title),
                                    icon_size=16,
                                    icon_color=ft.Colors.RED
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ], tight=True),
                        padding=10,
                        width=150,
                    ),
                    elevation=2,
                )
                saved_topics_row.controls.append(topic_card)
            
            main_view_content.controls.append(saved_topics_row)
            main_view_content.controls.append(ft.Divider(height=20))
        
        if not app_state.chapters:
            # Check for missing dependencies
            missing_deps = check_dependencies()
            if missing_deps:
                main_view_content.controls.extend([
                    ft.Text("Upload a document to get started.", size=18, text_align=ft.TextAlign.CENTER),
                    ft.Text("", size=8),
                    ft.Text("⚠️ Some file formats may not work due to missing dependencies:", size=14, color=ft.Colors.AMBER),
                    ft.Text(f"Missing: {', '.join(missing_deps)}", size=12, color=ft.Colors.AMBER),
                    ft.Text("Install with: pip install " + " ".join(missing_deps), size=12, color=ft.Colors.BLUE),
                    ft.Text("", size=8),
                    ft.Text("Supported formats: TXT, PDF, DOCX, PPTX, EPUB", size=12, color=ft.Colors.GREEN)
                ])
            else:
                main_view_content.controls.extend([
                    ft.Text("Upload a document to get started.", size=18, text_align=ft.TextAlign.CENTER),
                    ft.Text("", size=8),
                    ft.Text("✅ All file format dependencies are installed!", size=14, color=ft.Colors.GREEN),
                    ft.Text("Supported formats: TXT, PDF, DOCX, PPTX, EPUB", size=12, color=ft.Colors.GREEN)
                ])
        else:
            # Show current topic info
            if app_state.current_topic_title:
                main_view_content.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"📖 Current Topic: {app_state.current_topic_title}", size=16, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                ft.Icons.SAVE,
                                tooltip="Update Saved Topic",
                                on_click=lambda e: save_current_topic(),
                                icon_size=20,
                                icon_color=ft.Colors.GREEN
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=10,
                        border=ft.border.all(1, ft.Colors.BLUE),
                        border_radius=10,
                    )
                )
            
            # Add save button for new topics
            if not app_state.current_topic_title:
                main_view_content.controls.append(
                    ft.Container(
                        content=ft.FilledButton(
                            "💾 Save as New Topic",
                            icon=ft.Icons.SAVE,
                            on_click=lambda e: save_current_topic(),
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=10)
                    )
                )
            
            main_view_content.controls.append(ft.Text(f"Found {len(app_state.chapters)} chapters. Select one to study:", size=20))
            for i, chapter in enumerate(app_state.chapters):
                main_view_content.controls.append(
                    ft.FilledButton(
                        text=f"{chapter['title']}",
                        icon=ft.Icons.MENU_BOOK,
                        on_click=lambda e, idx=i: navigate_to_study_options(idx),
                        width=400,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                    )
                )
        page.update()

    # --- Navigation Logic ---
    def navigate_to_home(e=None):
        study_options_view.visible = False
        flashcard_view.visible = False
        quiz_view.visible = False
        test_view.visible = False
        main_view_content.visible = True
        back_button.visible = False
        page.update()

    def navigate_to_study_options_from_views(e=None):
        """Navigate back to study options for the current chapter"""
        if app_state.current_chapter_index is not None:
            navigate_to_study_options(app_state.current_chapter_index)
        else:
            navigate_to_home()

    back_button = ft.IconButton(ft.Icons.ARROW_BACK, on_click=navigate_to_study_options_from_views, visible=False, tooltip="Back to Study Options")

    def navigate_to_study_options(chapter_index: int):
        app_state.set_current_chapter(chapter_index)  # Remember current chapter
        chapter = app_state.chapters[chapter_index]
        
        def on_flashcards_click(e, ch_content=chapter['content']):
            page.run_task(navigate_to_flashcards, ch_content)
        
        def on_quiz_click(e, ch_content=chapter['content']):
            page.run_task(navigate_to_quiz, ch_content)
        
        def on_test_click(e, ch_content=chapter['content']):
            page.run_task(navigate_to_test, ch_content)
        
        study_options_view.controls.clear()
        study_options_view.controls.extend([
            ft.Text(f"Studying: {chapter['title']}", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Choose a study method:", size=18),
            ft.FilledButton("Flashcards", icon=ft.Icons.STYLE, on_click=on_flashcards_click, width=250),
            ft.FilledButton("Quiz", icon=ft.Icons.QUIZ, on_click=on_quiz_click, width=250),
            ft.FilledButton("Test", icon=ft.Icons.ASSIGNMENT, on_click=on_test_click, width=250),
        ])

        main_view_content.visible = False
        flashcard_view.visible = False
        quiz_view.visible = False
        test_view.visible = False
        study_options_view.visible = True
        back_button.visible = True # Show back button
        page.update()

    async def navigate_to_flashcards(chapter_content: str):
        flashcards = await generate_flashcards_from_text(chapter_content)
        app_state.set_flashcards(flashcards)
        
        study_options_view.visible = False
        quiz_view.visible = False
        test_view.visible = False
        flashcard_view.visible = True
        update_flashcard_ui()
        page.update()

    async def navigate_to_quiz(chapter_content: str):
        """Navigate to quiz mode and generate quiz questions"""
        show_loading(True)
        try:
            quiz_data = await ai_generator.generate_quiz(chapter_content)
            app_state.set_quiz(quiz_data)
            show_loading(False)
            
            study_options_view.visible = False
            flashcard_view.visible = False
            test_view.visible = False
            quiz_view.visible = True
            build_quiz_ui()
            page.update()
        except Exception as e:
            show_loading(False)
            print(f"Error generating quiz: {e}")

    async def navigate_to_test(chapter_content: str):
        """Navigate to test mode and generate test questions"""
        show_loading(True)
        try:
            test_data = await ai_generator.generate_test(chapter_content)
            app_state.set_test(test_data)
            show_loading(False)
            
            study_options_view.visible = False
            flashcard_view.visible = False
            quiz_view.visible = False
            test_view.visible = True
            build_test_ui()
            page.update()
        except Exception as e:
            show_loading(False)
            print(f"Error generating test: {e}")

    # --- File Upload Logic ---
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            try:
                # Show loading while processing
                show_loading(True)
                
                # Process the file using the new processor
                processor = FileProcessor()
                organizer = ContentOrganizer()
                
                # Check if file format is supported
                if not processor.is_supported(file_path):
                    show_loading(False)
                    show_snack_bar(f"Unsupported file format. Supported formats: {', '.join(get_supported_extensions())}", ft.Colors.RED_400)
                    return
                
                # Process the file
                processed_content = processor.process_file(file_path)
                
                # Organize into chapters
                chapter_objects = organizer.organize_into_chapters(processed_content)
                
                # Convert to the format expected by the app
                chapters = []
                for chapter_obj in chapter_objects:
                    chapters.append({
                        "title": chapter_obj.title,
                        "content": chapter_obj.content
                    })
                
                app_state.set_chapters(chapters)
                app_state.current_topic_title = ""  # Reset topic title for new upload
                show_loading(False)
                
                # Rebuild the main view with the list of chapters
                build_chapter_list_view()
                
                # Show success message
                show_snack_bar(f"Successfully processed {len(chapters)} chapters from {processed_content.file_type.upper()} file", ft.Colors.GREEN_400)

            except Exception as ex:
                show_loading(False)
                show_snack_bar(f"Error processing file: {str(ex)}", ft.Colors.RED_400)

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # --- Flashcard UI and Logic ---
    card_is_flipped = False
    
    def flip_card(e):
        nonlocal card_is_flipped
        if card_is_flipped:
            flashcard_container.content = card_term
            card_is_flipped = False
        else:
            flashcard_container.content = card_definition
            card_is_flipped = True
        page.update()

    card_term = ft.Text("", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    card_definition = ft.Text("", size=18, text_align=ft.TextAlign.CENTER, italic=True)
    
    flashcard_container = ft.Container(
        content=card_term, # Start with the term
        width=400,
        height=250,
        alignment=ft.alignment.center,
        padding=20,
        on_click=flip_card,
    )
    
    flashcard_card = ft.Card(
        content=flashcard_container,
        elevation=10,
    )

    progress_text = ft.Text("1/10", size=16)

    def update_flashcard_ui():
        nonlocal card_is_flipped
        card = app_state.get_current_flashcard()
        if card:
            card_term.value = card['term']
            card_definition.value = card['definition']
            flashcard_container.content = card_term # Reset to show term first
            card_is_flipped = False
            progress_text.value = f"{app_state.current_flashcard_index + 1} / {len(app_state.current_flashcards)}"
        else:
            card_term.value = "No more cards!"
            card_definition.value = "Go back to study another chapter."
            flashcard_container.content = card_term
            card_is_flipped = False
        page.update()

    def show_prev_card(e):
        if app_state.prev_flashcard():
            update_flashcard_ui()

    def show_next_card(e):
        if app_state.next_flashcard():
            update_flashcard_ui()

    flashcard_view.controls.extend([
        ft.Text("Flashcards", size=24, weight=ft.FontWeight.BOLD),
        progress_text,
        flashcard_card,
        ft.Row(
            [
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=show_prev_card, tooltip="Previous"),
                ft.FilledButton("Flip Card", icon=ft.Icons.SWAP_HORIZ, on_click=flip_card),
                ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=show_next_card, tooltip="Next")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    ])

    # --- Quiz UI and Logic ---
    def build_quiz_ui():
        """Build the quiz interface"""
        quiz_view.controls.clear()
        
        if not app_state.current_quiz:
            quiz_view.controls.append(ft.Text("No quiz available", size=18))
            return
        
        quiz_data = app_state.current_quiz
        quiz_view.controls.append(ft.Text(quiz_data.get('title', 'Quiz'), size=24, weight=ft.FontWeight.BOLD))
        
        # Add questions
        for i, question in enumerate(quiz_data['questions']):
            question_container = ft.Container(
                content=ft.Column([
                    ft.Text(f"Question {i+1}: {question['question']}", size=16, weight=ft.FontWeight.W_500),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value=str(j), label=option) for j, option in enumerate(question['options'])
                        ]),
                        on_change=lambda e, q_idx=i: handle_quiz_answer(q_idx, int(e.control.value) if e.control.value else 0)
                    )
                ]),
                padding=20,
                margin=ft.margin.symmetric(vertical=10),
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=10,
            )
            quiz_view.controls.append(question_container)
        
        # Submit button
        quiz_view.controls.append(
            ft.Container(
                content=ft.FilledButton("Submit Quiz", icon=ft.Icons.CHECK, on_click=submit_quiz, width=200),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=20)
            )
        )

    def handle_quiz_answer(question_index: int, answer_index: int):
        """Handle quiz answer selection"""
        if question_index < len(app_state.quiz_answers):
            app_state.quiz_answers[question_index] = answer_index

    def submit_quiz(e):
        """Submit quiz and show results"""
        if not app_state.current_quiz:
            return
        
        # Calculate score
        correct_answers = 0
        total_questions = len(app_state.current_quiz['questions'])
        
        for i, question in enumerate(app_state.current_quiz['questions']):
            if i < len(app_state.quiz_answers) and app_state.quiz_answers[i] == question['correct_answer']:
                correct_answers += 1
        
        app_state.quiz_score = correct_answers
        
        # Show results
        show_quiz_results(correct_answers, total_questions)

    def show_quiz_results(correct: int, total: int):
        """Display quiz results"""
        quiz_view.controls.clear()
        
        percentage = (correct / total) * 100 if total > 0 else 0
        color = ft.Colors.GREEN if percentage >= 70 else ft.Colors.ORANGE if percentage >= 50 else ft.Colors.RED
        
        quiz_view.controls.extend([
            ft.Text("Quiz Results", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Score: {correct}/{total}", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Percentage: {percentage:.1f}%", size=18, color=color),
                ]),
                alignment=ft.alignment.center,
                padding=20,
                border=ft.border.all(2, color),
                border_radius=10,
            ),
            ft.FilledButton("Try Again", icon=ft.Icons.REFRESH, on_click=lambda e: build_quiz_ui(), width=200),
            ft.OutlinedButton("Back to Study Options", icon=ft.Icons.ARROW_BACK, on_click=navigate_to_study_options_from_views, width=200),
        ])
        page.update()

    # --- Test UI and Logic ---
    def build_test_ui():
        """Build the test interface"""
        test_view.controls.clear()
        
        if not app_state.current_test:
            test_view.controls.append(ft.Text("No test available", size=18))
            return
        
        test_data = app_state.current_test
        test_view.controls.append(ft.Text(test_data.get('title', 'Test'), size=24, weight=ft.FontWeight.BOLD))
        
        # Add questions
        for i, question in enumerate(test_data['questions']):
            question_type = question.get('type', 'multiple_choice')
            
            question_container = ft.Container(
                content=ft.Column([
                    ft.Text(f"Question {i+1}: {question['question']}", size=16, weight=ft.FontWeight.W_500),
                    ft.Text(f"Type: {question_type.replace('_', ' ').title()}", size=12, color=ft.Colors.BLUE_GREY),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value=str(j), label=option) for j, option in enumerate(question['options'])
                        ]),
                        on_change=lambda e, q_idx=i: handle_test_answer(q_idx, int(e.control.value) if e.control.value else 0)
                    )
                ]),
                padding=20,
                margin=ft.margin.symmetric(vertical=10),
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=10,
            )
            test_view.controls.append(question_container)
        
        # Submit button
        test_view.controls.append(
            ft.Container(
                content=ft.FilledButton("Submit Test", icon=ft.Icons.ASSIGNMENT_TURNED_IN, on_click=submit_test, width=200),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=20)
            )
        )

    def handle_test_answer(question_index: int, answer_index: int):
        """Handle test answer selection"""
        if question_index < len(app_state.test_answers):
            app_state.test_answers[question_index] = answer_index

    def submit_test(e):
        """Submit test and show results"""
        if not app_state.current_test:
            return
        
        # Calculate score
        correct_answers = 0
        total_questions = len(app_state.current_test['questions'])
        
        for i, question in enumerate(app_state.current_test['questions']):
            if i < len(app_state.test_answers) and app_state.test_answers[i] == question['correct_answer']:
                correct_answers += 1
        
        app_state.test_score = correct_answers
        
        # Show detailed results
        show_test_results(correct_answers, total_questions)

    def show_test_results(correct: int, total: int):
        """Display detailed test results"""
        test_view.controls.clear()
        
        percentage = (correct / total) * 100 if total > 0 else 0
        color = ft.Colors.GREEN if percentage >= 80 else ft.Colors.ORANGE if percentage >= 60 else ft.Colors.RED
        grade = "A" if percentage >= 90 else "B" if percentage >= 80 else "C" if percentage >= 70 else "D" if percentage >= 60 else "F"
        
        test_view.controls.extend([
            ft.Text("Test Results", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Score: {correct}/{total}", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Percentage: {percentage:.1f}%", size=18, color=color),
                    ft.Text(f"Grade: {grade}", size=20, weight=ft.FontWeight.BOLD, color=color),
                ]),
                alignment=ft.alignment.center,
                padding=20,
                border=ft.border.all(2, color),
                border_radius=10,
            )
        ])

        # Show detailed breakdown
        test_view.controls.append(ft.Text("Detailed Results:", size=18, weight=ft.FontWeight.BOLD))
        
        if app_state.current_test:
            for i, question in enumerate(app_state.current_test['questions']):
                user_answer = app_state.test_answers[i] if i < len(app_state.test_answers) else None
                correct_answer = question['correct_answer']
                is_correct = user_answer == correct_answer
                
                result_color = ft.Colors.GREEN if is_correct else ft.Colors.RED
                status_icon = ft.Icons.CHECK_CIRCLE if is_correct else ft.Icons.CANCEL
                
                question_result = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(status_icon, color=result_color),
                            ft.Text(f"Q{i+1}: {question['question'][:50]}...", size=14, weight=ft.FontWeight.W_500)
                        ]),
                        ft.Text(f"Your answer: {question['options'][user_answer] if user_answer is not None else 'No answer'}", size=12),
                        ft.Text(f"Correct answer: {question['options'][correct_answer]}", size=12, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Explanation: {question.get('explanation', 'No explanation available')}", size=12, italic=True)
                    ]),
                    padding=15,
                    margin=ft.margin.symmetric(vertical=5),
                    border=ft.border.all(1, result_color),
                    border_radius=5,
                )
                test_view.controls.append(question_result)
        
        test_view.controls.extend([
            ft.Container(height=20),  # Spacer
            ft.FilledButton("Retake Test", icon=ft.Icons.REFRESH, on_click=lambda e: build_test_ui(), width=200),
            ft.OutlinedButton("Back to Study Options", icon=ft.Icons.ARROW_BACK, on_click=navigate_to_study_options_from_views, width=200),
        ])
        page.update()

    # --- App Bar ---
    app_bar = ft.AppBar(
        leading=back_button,
        title=ft.Text("AI Study Buddy"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE,
        actions=[
            ft.IconButton(
                ft.Icons.UPLOAD_FILE, 
                on_click=lambda _: file_picker.pick_files(
                    allow_multiple=False, 
                    allowed_extensions=["txt", "pdf", "docx", "doc", "pptx", "ppt", "epub"]
                ), 
                tooltip="Upload a Book (TXT, PDF, DOCX, PPTX, EPUB)"
            )
        ],
    )

    loading_indicator = ft.ProgressRing(visible=False)

    # --- Initialize Loading Screen ---
    async def init_app():
        """Initialize the app with loading screen"""
        await asyncio.sleep(2)  # Show loading screen for 2 seconds
        loading_screen.visible = False
        main_view_content.visible = True
        build_chapter_list_view()  # Initial build
        page.update()

    # --- Initial Page Load ---
    page.appbar = app_bar
    page.add(
        loading_indicator,
        loading_screen,
        main_view_content,
        study_options_view,
        flashcard_view,
        quiz_view,
        test_view,
    )
    
    # Start the initialization
    page.run_task(init_app)

# To run the app
if __name__ == "__main__":
    ft.app(target=main)
