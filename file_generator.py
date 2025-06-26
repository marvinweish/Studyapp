import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pptx import Presentation
from pptx.util import Inches as PPTXInches
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from ebooklib import epub
from random import choice, randint

# --- Configuration ---
OUTPUT_DIR = "test_files"

# Load LOREM_IPSUM from input.txt file
def load_lorem_ipsum():
    """Load LOREM_IPSUM text from input.txt file."""
    try:
        with open('input.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fallback text if input.txt doesn't exist
        return "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

LOREM_IPSUM = load_lorem_ipsum()

def create_output_directory():
    """Creates the output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")
    else:
        print(f"Directory already exists: {OUTPUT_DIR}")

# --- PDF Generation Functions ---

def generate_pdf_simple_text():
    """Generates a simple PDF with plain text."""
    filename = os.path.join(OUTPUT_DIR, "simple_text.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("This is a simple PDF document for testing text extraction from a PDF file.", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("It has no images or complex formatting, just plain paragraphs for basic testing.", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(LOREM_IPSUM, styles['Normal']))

    doc.build(story)
    print(f"Generated {filename}")

def generate_pdf_formatted_document():
    """Generates a PDF with headings, lists, bold/italic text."""
    filename = os.path.join(OUTPUT_DIR, "formatted_document.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    h1_style = styles['h1']
    h2_style = styles['h2']
    normal_style = styles['Normal']

    # Title
    story.append(Spacer(1, 0.3 * inch))
    story.append(Spacer(1, 0.3 * inch))

    # Chapter 1
    story.append(Paragraph("Chapter 1: Introduction", h2_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("This chapter introduces various formatting elements that your study app should be able to extract correctly. We will include **bold text**, *italic text*, and a combination of both.", normal_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(LOREM_IPSUM, normal_style))
    story.append(Spacer(1, 0.2 * inch))

    # Lists
    story.append(Paragraph("Here is a list of items:", normal_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(ListFlowable(
        [
            Paragraph("Item One with some <b>bold</b> text.", normal_style),
            Paragraph("Item Two with <i>italic</i> text.", normal_style),
            Paragraph("Item Three with <font color='red'>colored</font> text.", normal_style),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletAlign='left',
        indent=36,
        bulletIndent=18
    ))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("And a numbered list:", normal_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(ListFlowable(
        [
            Paragraph("First step.", normal_style),
            Paragraph("Second step.", normal_style),
            Paragraph("Third step.", normal_style),
        ],
        bulletType='1',
        start='1',
        bulletAlign='left',
        indent=36,
        bulletIndent=18
    ))
    story.append(Spacer(1, 0.2 * inch))

    # Add more pages
    for i in range(2, 5):
        story.append(Spacer(1, 1 * inch)) # New page separator
        story.append(Paragraph(f"Chapter {i}: More Content", h2_style))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(LOREM_IPSUM * randint(1, 3), normal_style))
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)
    print(f"Generated {filename}")

def generate_pdf_mixed_content():
    """Generates a PDF with text, an image, and a table."""
    filename = os.path.join(OUTPUT_DIR, "mixed_content.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Text
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(LOREM_IPSUM, styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))

    # Placeholder Image (you'd replace this with a real image path)
    # Placeholder Image (you'd replace this with a real image path)
    # For a placeholder, we can create a tiny blank image or refer to a non-existent one
    # To make this runnable without an image file, let's skip actual image embedding
    # or create a dummy 1x1 image on the fly. For simplicity, I'll use a placeholder URL if supported,
    # or just omit it for this runnable example as reportlab expects a local file.
    # A better approach would be to create a simple dummy image.
    story.append(Paragraph("--- Placeholder for an Image ---", styles['h3']))
    story.append(Spacer(1, 0.2 * inch))
   
    # If you have an image, uncomment and replace 'path/to/your/image.png'
    # try:
    #     img = Image("path/to/your/image.png", width=2*Inches, height=2*Inches)
    #     story.append(img)
    #     story.append(Spacer(1, 0.2 * Inches))
    # except Exception as e:
    #     print(f"Could not add image: {e}. Please provide a valid image path if desired.")


    # Table
    data = [
        ['Header 1', 'Header 2', 'Header 3'],
        ['Row 1, Col 1', 'Row 1, Col 2', 'Row 1, Col 3'],
        ['Row 2, Col 1', 'Row 2, Col 2', 'Row 2, Col 3'],
        ['Row 3, Col 1', 'Row 3, Col 2', 'Row 3, Col 3 with more text to wrap']
    ]
    table = Table(data, colWidths=[2*inch, 2*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("This is additional text after the table.", styles['Normal']))

    doc.build(story)
    print(f"Generated {filename}")

# --- Word Document Generation Functions (.docx) ---

def generate_docx_plain_text():
    """Generates a simple Word document with plain text."""
    filename = os.path.join(OUTPUT_DIR, "plain_text.docx")
    document = Document()
    document.add_heading('Simple Text Document', level=1)
    document.add_paragraph('This is a simple Word document with plain text for testing purposes.')
    document.add_paragraph('It contains several paragraphs without any special formatting.')
    for _ in range(5):
        document.add_paragraph(LOREM_IPSUM)
    document.save(filename)
    print(f"Generated {filename}")

def generate_docx_formatted_document():
    """Generates a Word document with various formatting elements."""
    filename = os.path.join(OUTPUT_DIR, "formatted_document.docx")
    document = Document()

    document.add_heading('Formatted Document Test', level=0) # Main Title

    # Sub-heading
    document.add_heading('Section 1: Introduction', level=1)
    p = document.add_paragraph()
    p.add_run('This section demonstrates various text formatting options. ')
    p.add_run('Here is some ').bold = True
    p.add_run('bold text').bold = True
    p.add_run(' and some ').italic = True
    p.add_run('italic text').italic = True
    p.add_run('. We also have a combination of ').bold = True; p.add_run('bold ').italic = True; p.add_run('and italic.').bold = True; p.add_run(' This sentence has different ').font.size = Pt(18); p.add_run('font size.')

    # Bulleted list
    document.add_heading('Section 2: Lists', level=2)
    document.add_paragraph('Item one', style='List Bullet')
    document.add_paragraph('Item two', style='List Bullet')
    document.add_paragraph('Item three', style='List Bullet 2') # Different level bullet

    # Numbered list
    document.add_paragraph('First step', style='List Number')
    document.add_paragraph('Second step', style='List Number')

    # Table
    document.add_heading('Section 3: Data Table', level=2)
    table = document.add_table(rows=4, cols=3)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Header 1'
    hdr_cells[1].text = 'Header 2'
    hdr_cells[2].text = 'Header 3'

    for i in range(1, 4):
        cells = table.rows[i].cells
        cells[0].text = f'Row {i}, Col 1'
        cells[1].text = f'Row {i}, Col 2'
        cells[2].text = f'Row {i}, Col 3 with some more text to wrap.'

    document.add_paragraph(LOREM_IPSUM)

    document.save(filename)
    print(f"Generated {filename}")

def generate_docx_long_document():
    """Generates a multi-page Word document with multiple sections."""
    filename = os.path.join(OUTPUT_DIR, "long_document.docx")
    document = Document()
    document.add_heading('Long Document Test for App Performance', level=0)

    # Section 1
    document.add_heading('Chapter 1: The Beginning', level=1)
    for _ in range(10):
        document.add_paragraph(LOREM_IPSUM * randint(1, 3))
    document.add_page_break() # Force a new page

    # Section 2
    document.add_heading('Chapter 2: The Middle Part', level=1)
    for _ in range(15):
        document.add_paragraph(LOREM_IPSUM * randint(1, 2))
    document.add_page_break()

    # Section 3 with a "simulated" footnote (python-docx doesn't directly support footnotes)
    document.add_heading('Chapter 3: Conclusion and References', level=1)
    document.add_paragraph("This chapter concludes our long document test. It includes a reference that might appear as a footnote in a rendered document, although python-docx does not natively support true footnotes. Your app should still be able to extract all main body text.")
    p = document.add_paragraph('Here is some text with a simulated reference marker. [1]')
    p.add_run('This is additional text.')

    # You could add a section at the end for "Notes" or "References"
    document.add_heading('Appendix: Notes', level=2)
    document.add_paragraph('[1] This is the content of a simulated footnote or endnote. It provides additional information relevant to the preceding text.')
    document.add_paragraph(LOREM_IPSUM * 5) # More content to ensure it's long

    document.save(filename)
    print(f"Generated {filename}")

# --- PowerPoint Presentation Generation Functions (.pptx) ---

def generate_pptx_simple_presentation():
    """Generates a simple PowerPoint presentation."""
    filename = os.path.join(OUTPUT_DIR, "simple_presentation.pptx")
    prs = Presentation()

    # Slide 1: Title Slide
    slide_layout = prs.slide_layouts[0] # Title slide layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    if title:
        title.text = "Simple Presentation Test"
    try:
        subtitle.text = "For Study App Text Extraction" # type: ignore
    except:
        pass

    # Slide 2: Title and Content
    slide_layout = prs.slide_layouts[1] # Title and Content layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    body = slide.shapes.placeholders[1]
    if title:
        title.text = "Key Points"
    try:
        tf = body.text_frame # type: ignore
        p = tf.add_paragraph()
        p.text = "This slide contains important bullet points."
        p.level = 0
        p = tf.add_paragraph()
        p.text = "Point 1: Basic text extraction"
        p.level = 1
        p = tf.add_paragraph()
        p.text = "Point 2: Ensure all text boxes are read."
        p.level = 1
    except:
        pass

    # Slide 3: Another Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    body = slide.shapes.placeholders[1]
    if title:
        title.text = "Conclusion"
    try:
        tf = body.text_frame # type: ignore
        p = tf.add_paragraph()
        p.text = "This presentation serves as a basic test file."
        p.level = 0
        p = tf.add_paragraph()
        p.text = "Your app should successfully extract all text from these slides."
        p.level = 1
    except:
        pass

    prs.save(filename)
    print(f"Generated {filename}")

def generate_pptx_complex_presentation():
    """Generates a PowerPoint presentation with various layouts and an image."""
    filename = os.path.join(OUTPUT_DIR, "complex_presentation.pptx")
    prs = Presentation()

    # Slide 1: Title Slide
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    if title:
        title.text = "Complex Presentation Example"
    try:
        subtitle.text = "Testing Advanced Text & Layouts" # type: ignore
    except:
        pass

    # Slide 2: Title and Content with different text
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    body = slide.shapes.placeholders[1]
    if title:
        title.text = "Detailed Section A"
    try:
        tf = body.text_frame # type: ignore
        p = tf.add_paragraph()
        p.text = "This slide includes multiple paragraphs of text to test comprehensive extraction."
        p.level = 0
        p = tf.add_paragraph()
        p.text = LOREM_IPSUM
        p.level = 0
    except:
        pass

    # Slide 3: Title Only (no body text placeholder)
    slide_layout = prs.slide_layouts[5] # Title Only layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    if title:
        title.text = "Important Heading Only"
    # Add a custom text box
    try:
        left = top = width = height = PPTXInches(1)
        txBox = slide.shapes.add_textbox(left, top + PPTXInches(1), PPTXInches(5), PPTXInches(2))
        tf = txBox.text_frame
        p = tf.add_paragraph()
        p.text = "This is a custom text box. Your app needs to find text not just in default placeholders."
    except Exception:
        # Fallback if textbox creation fails
        pass

    # Slide 4: Blank slide with an image and text box
    slide_layout = prs.slide_layouts[6] # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    # Add a placeholder for an image. Real image path required for actual image.
    # For a runnable example, we will just add text stating where an image would be.
    try:
        left = PPTXInches(1)
        top = PPTXInches(1)
        width = PPTXInches(4)
        height = PPTXInches(3)
        slide.shapes.add_textbox(left, top, width, height).text_frame.text = "--- Placeholder for an Image Here ---"
        slide.shapes.add_textbox(left + width + PPTXInches(0.5), top, width, height).text_frame.text = "Text next to the image placeholder."
    except Exception:
        # Fallback if textbox creation fails
        pass

    # Slide 5: Title and Two Content
    slide_layout = prs.slide_layouts[3] # Title and Two Content layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    if title:
        title.text = "Comparison"

    left_body = slide.shapes.placeholders[1]
    try:
        left_tf = left_body.text_frame
        left_tf.text = "Left column content:\n- Point A\n- Point B"
    except:
        pass

    right_body = slide.shapes.placeholders[2]
    try:
        right_tf = right_body.text_frame
        right_tf.text = "Right column content:\n- Point X\n- Point Y"
    except:
        pass

    prs.save(filename)
    print(f"Generated {filename}")

# --- EPUB Generation Functions ---

def generate_epub_simple_novel():
    """Generates a simple EPUB file with text and chapters."""
    filename = os.path.join(OUTPUT_DIR, "simple_novel.epub")
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier('id123456')
    book.set_title('Simple Novel Test')
    book.set_language('en')
    book.add_author('Test Author')

    # Create chapters
    c1 = epub.EpubHtml(title='Chapter 1: The Beginning', file_name='chap_01.xhtml', lang='en')
    c1.content = '<h1>Chapter 1: The Beginning</h1><p>' + LOREM_IPSUM + '</p><p>' + LOREM_IPSUM + '</p>'

    c2 = epub.EpubHtml(title='Chapter 2: The Middle', file_name='chap_02.xhtml', lang='en')
    c2.content = '<h1>Chapter 2: The Middle</h1><p>' + LOREM_IPSUM + '</p><p>' + LOREM_IPSUM + '</p>'

    c3 = epub.EpubHtml(title='Chapter 3: The End', file_name='chap_03.xhtml', lang='en')
    c3.content = '<h1>Chapter 3: The End</h1><p>' + LOREM_IPSUM + '</p><p>' + LOREM_IPSUM + '</p>'

    # Add chapters to the book
    book.add_item(c1)
    book.add_item(c2)
    book.add_item(c3)

    # Define Table of Contents
    book.toc = [epub.Link('chap_01.xhtml', 'Chapter 1', 'intro'),
                epub.Link('chap_02.xhtml', 'Chapter 2', 'middle'),
                epub.Link('chap_03.xhtml', 'Chapter 3', 'end')]

    # Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define spine (order of chapters)
    book.spine = ['nav', c1, c2, c3]

    # Write the EPUB file
    epub.write_epub(filename, book, {})
    print(f"Generated {filename}")

def generate_epub_formatted_book():
    """Generates an EPUB file with formatted text and footnotes."""
    filename = os.path.join(OUTPUT_DIR, "formatted_book.epub")
    book = epub.EpubBook()

    book.set_identifier('id789012')
    book.set_title('Formatted Book Test')
    book.set_language('en')
    book.add_author('Advanced Author')

    # Chapter 1 with formatting
    c1 = epub.EpubHtml(title='Introduction', file_name='chap_01_intro.xhtml', lang='en')
    c1.content = """
    <h1>Introduction</h1>
    <p>This chapter contains <strong>bold text</strong>, <em>italic text</em>, and a mix of <strong><em>both</em></strong> to test your app's parsing capabilities.</p>
    <p>""" + LOREM_IPSUM + """</p>
    <p>Here is some text with a <a href="#footnote1" epub:type="footnote">simulated footnote</a>.
    And more text follows.</p>
    """

    # Chapter 2 with a list
    c2 = epub.EpubHtml(title='Key Concepts', file_name='chap_02_concepts.xhtml', lang='en')
    c2.content = """
    <h1>Key Concepts</h1>
    <p>We will discuss the following:</p>
    <ul>
        <li>Concept A: Detailed explanation.</li>
        <li>Concept B: Further insights.</li>
        <li>Concept C: Concluding remarks.</li>
    </ul>
    <p>""" + LOREM_IPSUM + """</p>
    """

    # Footnotes chapter (a common way to handle footnotes in EPUB)
    footnotes = epub.EpubHtml(title='Footnotes', file_name='footnotes.xhtml', lang='en')
    footnotes.content = """
    <h1>Footnotes</h1>
    <ol>
        <li id="footnote1">This is the content of footnote 1. It provides additional information for the main text.</li>
        <li id="footnote2">This is the content of footnote 2.</li>
    </ol>
    """

    book.add_item(c1)
    book.add_item(c2)
    book.add_item(footnotes)

    book.toc = [epub.Link('chap_01_intro.xhtml', 'Introduction', 'intro_id'),
                epub.Link('chap_02_concepts.xhtml', 'Key Concepts', 'concepts_id'),
                epub.Link('footnotes.xhtml', 'Footnotes', 'footnotes_id')]

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ['nav', c1, c2, footnotes]

    epub.write_epub(filename, book, {})
    print(f"Generated {filename}")

# --- Text File Generation Functions ---

def generate_txt_plain_text():
    """Generates a simple plain text file."""
    filename = os.path.join(OUTPUT_DIR, "plain_text.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("This is a simple plain text file for basic testing.\n")
        f.write("It contains multiple lines of unformatted text.\n\n")
        f.write(LOREM_IPSUM * 3)
    print(f"Generated {filename}")

def generate_txt_long_text():
    """Generates a large plain text file."""
    filename = os.path.join(OUTPUT_DIR, "long_text.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("This is a very large text file designed to test performance and memory handling.\n\n")
        # Write 5000 paragraphs of lorem ipsum to make it large
        for i in range(5000):
            f.write(f"Paragraph {i+1}: " + LOREM_IPSUM + "\n\n")
    print(f"Generated {filename}")

# --- Main Generation Function ---

def generate_all_test_files():
    """Generates all test files across different formats and complexities."""
    create_output_directory()

    print("\n--- Generating PDF Files ---")
    generate_pdf_simple_text()
    generate_pdf_formatted_document()
    generate_pdf_mixed_content()

    print("\n--- Generating Word Documents (.docx) ---")
    generate_docx_plain_text()
    generate_docx_formatted_document()
    generate_docx_long_document()

    print("\n--- Generating PowerPoint Presentations (.pptx) ---")
    generate_pptx_simple_presentation()
    generate_pptx_complex_presentation()

    print("\n--- Generating EPUB Files (.epub) ---")
    generate_epub_simple_novel()
    generate_epub_formatted_book()

    print("\n--- Generating Text Files (.txt) ---")
    generate_txt_plain_text()
    generate_txt_long_text()

    print(f"\nAll test files generated in the '{OUTPUT_DIR}' directory!")

if __name__ == "__main__":
    generate_all_test_files()
