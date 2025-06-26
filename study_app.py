import flet as ft
import re
import asyncio

# A simple class to hold the state of our application
class AppState:
    def __init__(self):
        self.chapters = []
        self.current_flashcards = []
        self.current_flashcard_index = 0

    def set_chapters(self, chapters):
        self.chapters = chapters

    def set_flashcards(self, flashcards):
        self.current_flashcards = flashcards
        self.current_flashcard_index = 0

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

def main(page: ft.Page):
    page.title = "AI Study Buddy"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.all(20)

    # --- Helper Functions ---
    def show_loading(show: bool):
        """Shows or hides a loading indicator."""
        loading_indicator.visible = show
        page.update()

    def parse_book_into_chapters(content: str) -> list[dict]:
        """
        Splits a book's text content into chapters.
        This is a simple implementation assuming chapters are marked with 'Chapter X'.
        """
        # Regex to find "Chapter" followed by a number or roman numeral
        chapter_pattern = re.compile(r'^(Chapter\s+(\d+|[IVXLCDM]+))', re.IGNORECASE | re.MULTILINE)
        
        # Find all chapter titles
        matches = list(chapter_pattern.finditer(content))
        
        if not matches:
            # If no chapters are found, treat the whole book as one chapter
            return [{"title": "Full Document", "content": content.strip()}]

        chapters = []
        for i, match in enumerate(matches):
            chapter_title = match.group(1).strip()
            start_index = match.end()
            
            # The end of the chapter is the start of the next one
            end_index = matches[i+1].start() if i + 1 < len(matches) else len(content)
            
            chapter_content = content[start_index:end_index].strip()
            chapters.append({"title": chapter_title, "content": chapter_content})
            
        return chapters

    async def generate_flashcards_from_text(chapter_content: str):
        """
        Uses the Gemini API to generate flashcards from text.
        NOTE: This is a placeholder for the actual API call.
        """
        show_loading(True)
        # In a real app, you would make an API call here.
        # For now, we simulate a delay and return mock data.
        await asyncio.sleep(3) # Simulate network latency
        
        # MOCK DATA - Replace this with your Gemini API call
        mock_flashcards = [
            {"term": "Flet", "definition": "A framework to build cross-platform apps in Python with Flutter."},
            {"term": "Python", "definition": "A high-level, general-purpose programming language."},
            {"term": "UI", "definition": "User Interface, the graphical layout of an application."},
            {"term": "Cross-Platform", "definition": "Software that can run on multiple operating systems like Windows, macOS, and Web."},
        ]
        show_loading(False)
        return mock_flashcards

    # --- UI Views ---
    
    # Placeholder for the main view content
    main_view_content = ft.Column(
        controls=[],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
    )

    def build_chapter_list_view():
        """Creates the list of chapters after a book is loaded."""
        main_view_content.controls.clear()
        
        if not app_state.chapters:
            main_view_content.controls.append(ft.Text("Upload a book to get started.", size=18, text_align=ft.TextAlign.CENTER))
        else:
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

    # View for flashcard interaction
    flashcard_view = ft.Column(
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    # View for study options (Flashcards, Quiz, etc.)
    study_options_view = ft.Column(
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    # --- Navigation Logic ---
    def navigate_to_home(e=None):
        study_options_view.visible = False
        flashcard_view.visible = False
        main_view_content.visible = True
        back_button.visible = False
        page.update()
    
    back_button = ft.IconButton(ft.Icons.ARROW_BACK, on_click=navigate_to_home, visible=False, tooltip="Back to Chapters")

    def navigate_to_study_options(chapter_index: int):
        chapter = app_state.chapters[chapter_index]
        
        def on_flashcards_click(e, ch_content=chapter['content']):
            page.run_task(navigate_to_flashcards, ch_content)
        
        study_options_view.controls.clear()
        study_options_view.controls.extend([
            ft.Text(f"Studying: {chapter['title']}", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Choose a study method:", size=18),
            ft.FilledButton("Flashcards", icon=ft.Icons.STYLE, on_click=on_flashcards_click, width=250),
            ft.OutlinedButton("Quiz (Coming Soon)", icon=ft.Icons.QUIZ, disabled=True, width=250),
            ft.OutlinedButton("Test (Coming Soon)", icon=ft.Icons.ASSIGNMENT, disabled=True, width=250),
        ])

        main_view_content.visible = False
        flashcard_view.visible = False
        study_options_view.visible = True
        back_button.visible = True # Show back button
        page.update()

    async def navigate_to_flashcards(chapter_content: str):
        flashcards = await generate_flashcards_from_text(chapter_content)
        app_state.set_flashcards(flashcards)
        
        study_options_view.visible = False
        flashcard_view.visible = True
        update_flashcard_ui()
        page.update()

    # --- File Upload Logic ---
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                chapters = parse_book_into_chapters(content)
                app_state.set_chapters(chapters)
                
                # Rebuild the main view with the list of chapters
                build_chapter_list_view()

            except Exception as ex:
                snack_bar = ft.SnackBar(ft.Text(f"Error reading file: {ex}"), bgcolor=ft.Colors.RED_400)
                page.overlay.append(snack_bar)
                snack_bar.open = True
                page.update()

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


    # --- App Bar ---
    app_bar = ft.AppBar(
        leading=back_button,
        title=ft.Text("AI Study Buddy"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE,
        actions=[
            ft.IconButton(ft.Icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["txt"]), tooltip="Upload a Book (.txt)")
        ],
    )

    loading_indicator = ft.ProgressRing(visible=False)

    # --- Initial Page Load ---
    page.appbar = app_bar
    page.add(
        loading_indicator,
        main_view_content,
        study_options_view,
        flashcard_view,
    )
    
    build_chapter_list_view() # Initial build

# To run the app
if __name__ == "__main__":
    ft.app(target=main)
