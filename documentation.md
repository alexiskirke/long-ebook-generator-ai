# long-ebook-generator-ai

**Author**: Alexis Kirke (narrative.layer)

## Overview

`long-ebook-generator-ai` is a Python library designed to generate long-form eBooks using AI-powered language models. It automates the process of creating structured book outlines, chapters, and converting them into an EPUB format, with optional Kindle compatibility. The package also supports AI-generated book covers and MathML conversion for LaTeX equations in the text.

The package integrates with OpenAI's API to generate book content based on customizable prompts, making it a powerful tool for authors, content creators, or developers looking to create AI-generated books.

## Features

- **AI-Powered Outline and Content Generation**: Automatically generate book outlines with chapters, sections, and subsections using OpenAI's GPT models.
- **EPUB Book Creation**: Convert AI-generated content into an EPUB format, compatible with major eReaders.
- **Customizable Book Structures**: Define the number of chapters, sections, and subsections for your book.
- **AI-Generated Book Covers**: Automatically generate a cover for your book using image generation AI models.
- **LaTeX Equation Support**: Convert LaTeX equations to MathML for display in the eBook.
- **Kindle Compatibility**: Optionally force compatibility with Amazon Kindle devices.

## Quick Start

Here's an example of how to generate an outline and an EPUB book using `long-ebook-generator-ai`.

Note that the total number of paragraphs will be num_chapters * sections_per_chapter * subsections_per_section * paras_per_section, so this can cost a number of dollars using GPT-4o for example. But is much lower cost using GPT-4o-mini. However results will be better with GPT-4o.

The model uses GPT-4o-mini by default. A short book will take under a minute, a book of 10 chapters can take quite a few minutes depending on the number of sections, sub_sections etc.

```python
from book_writer import BookWriter

writer = BookWriter(
    title="The AI Revolution", 
    openai_api_key=your_openai_api_key, 
    model="GPT-4o"
)

writer.generate_outline(
    num_chapters=5, 
    sections_per_chapter=3, 
    subsections_per_section=2, 
    paras_per_subsection=4
)

writer.generate_ebook(
    author="Your Name",
    generate_cover=True,
    force_kindle_compatibility=True
)
```

The package will generate an image for the cover and put the title and author on it.


# Detailed BookWriter Documentation

## Overview

The `BookWriter` class is designed to facilitate the end-to-end process of creating a book from an outline to generating an eBook (EPUB) file. The class leverages the `BookOutlineGenerator` to produce structured book outlines and the `OutlineEbookGenerator` to compile the content into an eBook format.

## Class: `BookWriter`

### Constructor: `__init__`

Initializes an instance of the `BookWriter` class, setting up the necessary components for book generation.

#### Syntax

```python
BookWriter(
    title: str,
    working_dir: str = 'outline_steps',
    openai_api_key: str = "",
    model: str = "gpt-4o-mini"
)
```

#### Parameters

- `title` (*str*): The title of the book.
- `working_dir` (*str*, optional): Directory for saving intermediate files during the outline generation process. Defaults to `'outline_steps'`.
- `openai_api_key` (*str*, optional): API key for OpenAI's language model. Required for generating content and cover images.
- `model` (*str*, optional): The OpenAI model to use for content generation. Defaults to `"gpt-4o-mini"`.

#### Attributes

- `title` (*str*): The title of the book.
- `model` (*str*): The selected OpenAI model for generating content.
- `openai_api_key` (*str*): OpenAI API key for connecting to the language model.
- `generator` (*BookOutlineGenerator*): Instance of `BookOutlineGenerator` to generate the book outline.
- `outline` (*Dict*): The generated outline of the book.
- `paragraph_style` (*str*): A predefined paragraph style to be applied during content generation. The style ensures modern, concise writing with occasional examples and stories.

### Public Methods

#### `generate_outline`

Generates the book outline using the `BookOutlineGenerator`.

##### Syntax

```python
generate_outline(
    num_chapters: int = 3,
    sections_per_chapter: int = 2,
    subsections_per_section: int = 3,
    paras_per_subsection: int = 3
) -> Dict
```

##### Parameters

- `num_chapters` (*int*, optional): Number of chapters to generate in the outline. Defaults to `3`.
- `sections_per_chapter` (*int*, optional): Number of sections per chapter. Defaults to `2`.
- `subsections_per_section` (*int*, optional): Number of subsections per section. Defaults to `3`.
- `paras_per_subsection` (*int*, optional): Number of paragraphs to generate per subsection. Defaults to `3`.

##### Returns

- `Dict`: The generated book outline.

##### Example

```python
book_writer = BookWriter(title="The Future of AI", openai_api_key="your_openai_api_key")
outline = book_writer.generate_outline(num_chapters=5, sections_per_chapter=3)
```

#### `generate_ebook`

Generates the eBook in EPUB format using the `OutlineEbookGenerator`. It compiles the outline into an eBook and optionally generates a cover image.

##### Syntax

```python
generate_ebook(
    author: str = 'Book Writer',
    generate_cover: bool = True,
    force_kindle_compatibility: bool = True,
    image_prompt: str = ''
)
```

##### Parameters

- `author` (*str*, optional): Author name to be included in the eBook. Defaults to `'Book Writer'`.
- `generate_cover` (*bool*, optional): Whether to generate a cover image for the eBook. Defaults to `True`.
- `force_kindle_compatibility` (*bool*, optional): Whether to force Kindle compatibility by including necessary navigation files. Defaults to `True`.
- `image_prompt` (*str*, optional): Custom prompt for generating the cover image using OpenAI's DALL-E. Defaults to an empty string.

##### Raises

- `ValueError`: If the outline has not been generated before calling this method.

##### Example

```python
book_writer.generate_ebook(
    author="John Doe",
    generate_cover=True,
    force_kindle_compatibility=True,
    image_prompt="A futuristic cityscape with advanced AI"
)
```

This method generates an EPUB file using the previously generated outline and saves it with a filename based on the book title.

### Private Attributes

- `paragraph_style` (*str*): A style guide for paragraph generation, ensuring modern, snappy writing with short sentences, limited adjectives and adverbs, and occasional examples and illustrative stories.

### Example Usage

```python
# Initialize the BookWriter with title and API key
book_writer = BookWriter(
    title="The Future of Technology",
    openai_api_key="your_openai_api_key"
)

# Generate the book outline
outline = book_writer.generate_outline(
    num_chapters=5,
    sections_per_chapter=3,
    subsections_per_section=4,
    paras_per_subsection=3
)

# Generate the eBook with a custom author name and cover image
book_writer.generate_ebook(
    author="Jane Doe",
    generate_cover=True,
    force_kindle_compatibility=True,
    image_prompt="A futuristic landscape showing human-AI collaboration"
)
```

### Dependencies

The `BookWriter` class depends on the following:

- **Third-Party Libraries**:
  - `BookOutlineGenerator`: Generates structured book outlines.
  - `OutlineEbookGenerator`: Converts outlines into eBooks and generates cover images.

Ensure that these libraries are installed and accessible.

## Notes

- **Custom Prompts**: You can provide a custom image prompt for the cover generation, or the class will generate a standard one based on the book title.
- **Outline Generation**: You must call `generate_outline` before attempting to generate the eBook. The outline is a prerequisite for compiling the content into EPUB format.
- **Kindle Compatibility**: The eBook generator can ensure Kindle compatibility by adding appropriate navigation files when `force_kindle_compatibility` is set to `True`.

---

*This documentation outlines the key functionality of the `BookWriter` class, which automates the process of generating book content and creating an eBook in EPUB format.*

# BookOutlineGenerator Documentation

## Overview

The `BookOutlineGenerator` class is designed to generate detailed book outlines using a language model (OpenAI's GPT-4O). It allows for the creation of structured outlines consisting of chapters, sections, subsections, and paragraphs. The class supports customizable parameters such as the number of chapters and sections, paragraph style, and more. The outline is saved progressively at different stages.

## Class: `BookOutlineGenerator`

### Constructor: `__init__`

Initializes the `BookOutlineGenerator` instance, setting up the working directory and the language model client.

#### Syntax

```python
BookOutlineGenerator(
    working_dir: str = 'outline_steps',
    openai_api_key: str = ""
)
```

#### Parameters

- `working_dir` (*str*, optional): Directory where the outline steps will be saved. Defaults to `'outline_steps'`.
- `openai_api_key` (*str*, optional): API key for OpenAI's language model.

#### Attributes

- `phrases_to_avoid` (*List[str]*): A list of phrases that the generator avoids in the output to maintain concise and clear content.
- `working_dir` (*str*): Directory where the intermediate outline steps are saved.
- `full_outline` (*Dict*): The full outline generated.
- `cumulative_tokens_sent` (*int*): Total tokens sent in requests to the language model.
- `cumulative_tokens_received` (*int*): Total tokens received from the language model.
- `encoder` (*tiktoken.Encoder*): Encoder for token counting.
- `total_sections` (*int*): Total sections in the outline (used for tracking progress).
- `completed_sections` (*int*): Completed sections in the outline (used for tracking progress).
- `llm_client` (*OpenAIClient*): Client for interacting with the OpenAI language model.

### Public Methods

#### `generate_styled_outline`

Generates a complete book outline based on the provided parameters.

##### Syntax

```python
generate_styled_outline(
    topic: str,
    num_chapters: int = 3,
    sections_per_chapter: int = 3,
    subsections_per_section: int = 3,
    paras_per_subsection: int = 1,
    paragraph_style: str = ''
) -> Dict
```

##### Parameters

- `topic` (*str*): The main topic of the book.
- `num_chapters` (*int*, optional): Number of chapters to generate. Defaults to `3`.
- `sections_per_chapter` (*int*, optional): Number of sections per chapter. Defaults to `3`.
- `subsections_per_section` (*int*, optional): Number of subsections per section. Defaults to `3`.
- `paras_per_subsection` (*int*, optional): Number of paragraphs per subsection. Defaults to `1`.
- `paragraph_style` (*str*, optional): Style guide for paragraph generation. Defaults to `''`.

##### Returns

- `Dict`: The complete book outline.

#### `save_outline`

Saves the generated outline to the specified working directory.

##### Syntax

```python
save_outline(depth_level: int)
```

##### Parameters

- `depth_level` (*int*): The depth level of the outline to save. For example, `0` for chapters, `1` for sections, etc.

### Private Methods

#### `_generate_chapters`

Generates chapter titles for the book based on the topic and the number of chapters.

##### Syntax

```python
_generate_chapters(topic: str, num_chapters: int)
```

##### Parameters

- `topic` (*str*): The main topic of the book.
- `num_chapters` (*int*): Number of chapters to generate.

#### `_generate_level1`

Generates level 1 sections (i.e., sections for each chapter) in the outline.

##### Syntax

```python
_generate_level1(sections_per_chapter: int)
```

##### Parameters

- `sections_per_chapter` (*int*): Number of sections to generate per chapter.

#### `_generate_level2`

Generates level 2 subsections (i.e., subsections for each section).

##### Syntax

```python
_generate_level2(subsections_per_section: int)
```

##### Parameters

- `subsections_per_section` (*int*): Number of subsections to generate per section.

#### `_generate_level3`

Generates paragraphs for each subsection, based on the paragraph style and number of paragraphs per subsection.

##### Syntax

```python
_generate_level3(paras_per_subsection: int, paragraph_style: str)
```

##### Parameters

- `paras_per_subsection` (*int*): Number of paragraphs to generate per subsection.
- `paragraph_style` (*str*): Style guide for paragraph generation.

#### `_send_request`

Sends a request to the language model and returns the generated text.

##### Syntax

```python
_send_request(prompt: str, is_title: bool) -> str
```

##### Parameters

- `prompt` (*str*): The prompt to send to the language model.
- `is_title` (*bool*): Whether the request is for generating titles (affects token limits).

##### Returns

- `str`: The generated text from the language model.

#### `_get_outline_context`

Returns the current outline context as a JSON string.

##### Syntax

```python
_get_outline_context() -> str
```

##### Returns

- `str`: The current outline context as a JSON string.

#### `_get_outline_context_summarised_paras`

Returns the current outline context with summarized paragraphs as a JSON string.

##### Syntax

```python
_get_outline_context_summarised_paras() -> str
```

##### Returns

- `str`: The outline context with summarized paragraphs.

#### `_print_progress`

Prints the progress of the outline generation based on the number of completed sections.

##### Syntax

```python
_print_progress()
```

#### `_count_total_sections`

Counts the total sections in the outline (used for progress tracking).

##### Syntax

```python
_count_total_sections(outline: Dict)
```

##### Parameters

- `outline` (*Dict*): The outline structure to count sections in.

### Dependencies

The `BookOutlineGenerator` class requires the following dependencies:

- **Standard Libraries**:
  - `os`: For directory operations.
  - `json`: For working with JSON data.
  - `tqdm`: For showing progress bars.
  - `copy`: For deep copying dictionaries.
- **Third-Party Libraries**:
  - `OpenAIClient`: A client for interacting with OpenAI's language model.
  - `tiktoken`: A library for encoding text and counting tokens.

Ensure that these dependencies are installed and accessible.

### Example Usage

```python
from book_outline_generator import BookOutlineGenerator

# Initialize the generator
generator = BookOutlineGenerator(openai_api_key="your_openai_api_key")

# Generate an outline for a book on AI with 5 chapters, 3 sections per chapter, etc.
outline = generator.generate_styled_outline(
    topic="Artificial Intelligence",
    num_chapters=5,
    sections_per_chapter=3,
    subsections_per_section=3,
    paras_per_subsection=2,
    paragraph_style="Use an informative and engaging style."
)

# Save the outline
generator.save_outline(depth_level=3)
```

This example generates a book outline on "Artificial Intelligence" with 5 chapters and saves the result to a specified directory.

## Notes

- **Custom Prompts**: Prompts sent to the language model can be customized to suit different styles and requirements. The model is capable of generating titles, sections, subsections, and paragraphs based on the given context.
- **Progress Tracking**: The class provides detailed progress tracking, including the number of tokens sent and received, as well as the current completion status of the outline generation.
- **Token Management**: The class includes token tracking to optimize usage and manage costs when interacting with OpenAI's API.

---

*This documentation provides an overview and usage guide for the `BookOutlineGenerator` class, which automates the creation of structured book outlines using GPT-based language models.*


# OutlineEbookGenerator Documentation

## Overview

The `OutlineEbookGenerator` class is designed to create eBooks from book outlines provided in a JSON format. It generates an EPUB file complete with chapters, a table of contents, and optional cover image generation using OpenAI's DALL-E API. The class supports LaTeX equations, converting them to MathML for proper rendering in eBook readers.

## Class: `OutlineEbookGenerator`

### Constructor: `__init__`

Initializes an instance of the `OutlineEbookGenerator` class.

#### Syntax

```python
OutlineEbookGenerator(
    json_file_path: str,
    book_title: str = 'Book Outline',
    book_author: str = 'Outline Generator',
    generate_cover: bool = False,
    force_kindle_compatibility: bool = False,
    override_image_prompt: str = '',
    openai_api_key: str = "",
    model: str = "gpt-4o-mini"
)
```

#### Parameters

- `json_file_path` (*str*): Path to the JSON file containing the outline data.
- `book_title` (*str*, optional): Title of the book. Defaults to `'Book Outline'`.
- `book_author` (*str*, optional): Author of the book. Defaults to `'Outline Generator'`.
- `generate_cover` (*bool*, optional): Whether to generate a cover image. Defaults to `False`.
- `force_kindle_compatibility` (*bool*, optional): Whether to force Kindle compatibility by adding an EPUB navigation file. Defaults to `False`.
- `override_image_prompt` (*str*, optional): Custom prompt for cover image generation using OpenAI's DALL-E. Defaults to `''`.
- `openai_api_key` (*str*, optional): OpenAI API key for generating the cover image. Required if `generate_cover` is `True`. Defaults to `""`.
- `model` (*str*, optional): OpenAI model to use for image generation. Options are `"gpt-4o-mini"` or `"gpt-4o"`. Defaults to `"gpt-4o-mini"`.

### Attributes

- `json_file_path` (*str*): Stores the path to the JSON file.
- `model` (*str*): OpenAI model to use.
- `outline_data` (*Dict*): The data loaded from the JSON file.
- `book_title` (*str*): Title of the book.
- `book_author` (*str*): Author of the book.
- `generate_cover` (*bool*): Indicates whether to generate a cover image.
- `force_kindle_compatibility` (*bool*): Indicates whether to force Kindle compatibility.
- `override_image_prompt` (*str*): Custom prompt for cover image generation.
- `openai_client` (*OpenAIClient*, optional): Client for interacting with OpenAI API. Initialized if `generate_cover` is `True`.

### Public Methods

#### `generate_ebook`

Generates the eBook from the outline data.

##### Syntax

```python
generate_ebook() -> epub.EpubBook
```

##### Returns

- `epub.EpubBook`: The generated eBook object.

#### `save_ebook`

Saves the generated eBook to a file.

##### Syntax

```python
save_ebook(output_file_path: str)
```

##### Parameters

- `output_file_path` (*str*): The path where the eBook will be saved.

### Private Methods

#### `_load_json`

Loads the JSON file containing the outline data.

##### Syntax

```python
_load_json() -> Dict
```

##### Returns

- `Dict`: The loaded outline data.

#### `_generate_section`

Recursively generates HTML content for a section of the eBook, including chapters and subsections.

##### Syntax

```python
_generate_section(section: Dict, depth: int, chapter_num: int) -> str
```

##### Parameters

- `section` (*Dict*): The section data.
- `depth` (*int*): The depth of the section in the outline hierarchy.
- `chapter_num` (*int*): The chapter number.

##### Returns

- `str`: The generated HTML content for the section.

#### `_generate_toc_section`

Generates HTML content for a section of the table of contents.

##### Syntax

```python
_generate_toc_section(section: Dict, chapter_num: int, depth: int) -> str
```

##### Parameters

- `section` (*Dict*): The section data.
- `chapter_num` (*int*): The chapter number.
- `depth` (*int*): The depth of the section in the outline hierarchy.

##### Returns

- `str`: The generated HTML content for the table of contents section.

#### `_generate_id`

Generates a valid HTML ID from a title by converting it to lowercase and replacing non-word characters with hyphens.

##### Syntax

```python
_generate_id(title: str) -> str
```

##### Parameters

- `title` (*str*): The title to convert.

##### Returns

- `str`: The generated HTML ID.

#### `_process_paragraph`

Processes a paragraph by converting LaTeX equations to MathML.

##### Syntax

```python
_process_paragraph(paragraph: str) -> str
```

##### Parameters

- `paragraph` (*str*): The paragraph to process.

##### Returns

- `str`: The processed paragraph with LaTeX equations converted to MathML.

#### `_latex_to_mathml`

Converts a LaTeX equation to MathML.

##### Syntax

```python
_latex_to_mathml(latex: str) -> str
```

##### Parameters

- `latex` (*str*): The LaTeX equation to convert.

##### Returns

- `str`: The converted MathML representation.

#### `_generate_cover_image`

Generates a cover image for the eBook with the title and author overlaid.

##### Syntax

```python
_generate_cover_image() -> bytes
```

##### Returns

- `bytes`: The generated cover image data.

##### Raises

- `RuntimeError`: If the OpenAI API call fails.

#### `_add_text_to_image`

Adds the title and author text to the cover image.

##### Syntax

```python
_add_text_to_image(img: Image.Image, title: str, author: str)
```

##### Parameters

- `img` (*Image.Image*): The image to add text to.
- `title` (*str*): The book title.
- `author` (*str*): The book author.

#### `_get_font_path`

Determines the font path based on the operating system.

##### Syntax

```python
_get_font_path() -> str
```

##### Returns

- `str`: The font path for the system.

##### Raises

- `OSError`: If the operating system is not supported.

#### `_find_optimal_font_size_and_wrap`

Finds the optimal font size and wraps the text to fit within the given dimensions.

##### Syntax

```python
_find_optimal_font_size_and_wrap(
    text: str,
    max_width: float,
    max_height: float,
    font_path: str
) -> Tuple[ImageFont.FreeTypeFont, List[str]]
```

##### Parameters

- `text` (*str*): The text to fit.
- `max_width` (*float*): Maximum width in pixels.
- `max_height` (*float*): Maximum height in pixels.
- `font_path` (*str*): Path to the font file.

##### Returns

- `Tuple[ImageFont.FreeTypeFont, List[str]]`: The font and list of wrapped text lines.

##### Raises

- `OSError`: If the font path is invalid.

#### `_draw_text_with_background`

Draws text with a background banner on the image.

##### Syntax

```python
_draw_text_with_background(
    img: Image.Image,
    lines: List[str],
    font: ImageFont.FreeTypeFont,
    y_position_ratio: float,
    bg_color: Tuple[int, int, int, int],
    text_color: Tuple[int, int, int, int],
    is_bottom: bool = False
)
```

##### Parameters

- `img` (*Image.Image*): The image to draw on.
- `lines` (*List[str]*): The lines of text to draw.
- `font` (*ImageFont.FreeTypeFont*): The font to use.
- `y_position_ratio` (*float*): Vertical position ratio for the text.
- `bg_color` (*Tuple[int, int, int, int]*): Background color in RGBA.
- `text_color` (*Tuple[int, int, int, int]*): Text color in RGBA.
- `is_bottom` (*bool*, optional): Whether to position the banner at the bottom. Defaults to `False`.

## Dependencies

The `OutlineEbookGenerator` class depends on the following external libraries:

- **Standard Libraries**:
  - `json`: For loading and handling JSON data.
  - `html`: For escaping HTML content.
  - `re`: For regular expressions.
  - `io`: For handling byte streams.
  - `platform`: For determining the operating system.
  - `textwrap`: For wrapping text.
- **Third-Party Libraries**:
  - `epub`: For creating EPUB books.
  - `PIL` (Python Imaging Library):
    - `Image`
    - `ImageDraw`
    - `ImageFont`
  - `requests`: For making HTTP requests (used in downloading images).
  - `latex2mathml`: For converting LaTeX equations to MathML.
  - `OpenAIClient`: A client class for interacting with the OpenAI API (not included in this snippet).
  
  *Note: You may need to install these libraries using `pip`.*

## Example Usage

```python
from outline_ebook_generator import OutlineEbookGenerator

# Initialize the generator with the path to the JSON outline file
generator = OutlineEbookGenerator(
    json_file_path='path_to_outline.json',
    book_title='My Book Title',
    book_author='Author Name',
    generate_cover=True,
    openai_api_key='your_openai_api_key',
    model='gpt-4o-mini'
)

# Generate and save the eBook
generator.save_ebook('output_book.epub')
```

This will generate an EPUB file named `output_book.epub` with the contents from `path_to_outline.json`, including a cover image generated using OpenAI's DALL-E API.

## Notes

- **OpenAI API Key**: Ensure you have a valid OpenAI API key if you wish to generate a cover image. Set `generate_cover=True` and provide the API key via `openai_api_key`.
- **Font Path**: The `_get_font_path` method automatically selects a font path based on the operating system. If the default paths do not work, you may need to adjust this method.
- **LaTeX Support**: The class supports LaTeX equations by converting them to MathML using the `latex2mathml` library. Install it via `pip install latex2mathml`.
- **Kindle Compatibility**: If you plan to read the eBook on a Kindle device, set `force_kindle_compatibility=True` to include necessary navigation files.
- **Dependencies**: Ensure all dependencies are installed, especially `PIL`, `requests`, and `epub` libraries.

## Limitations and Future Improvements

- **Error Handling**: Currently, error handling is minimal. Future versions could include more robust exception handling.
- **Customization**: Additional customization options for styling and formatting could be added.
- **Formats**: Support for generating eBooks in formats other than EPUB could be implemented.

---

*This documentation provides an overview and usage guide for the `OutlineEbookGenerator` class, facilitating the creation of eBooks from JSON-formatted outlines.*

# OutlineHTMLGenerator Documentation

## Overview

The `OutlineHTMLGenerator` class is designed to create HTML representations of book outlines. It parses the outline data from a JSON file and generates a styled HTML document for easy viewing.

## Class: `OutlineHTMLGenerator`

### Constructor: `__init__(self, json_file_path: str)`

Initializes an instance of `OutlineHTMLGenerator`.

#### Parameters:
- `json_file_path` (str): The path to the JSON file containing the book outline data.

### Attributes:
- `json_file_path` (str): Stores the path to the JSON file.
- `outline_data` (Dict): The data loaded from the JSON file.
- `summarized_paras_outline` (Optional): A placeholder for any future summarization of the outline (currently not used).
- `phrases_to_avoid` (List[str]): A list of phrases to avoid in the generated content to maintain clarity and avoid overused expressions.

### Private Method: `_load_json(self) -> Dict`

Loads the outline data from the JSON file provided during initialization.

#### Returns:
- `Dict`: A dictionary representing the book outline structure loaded from the JSON file.

### Public Method: `generate_html(self) -> str`

Generates the HTML content for the book outline based on the loaded JSON data.

#### Returns:
- `str`: The generated HTML content as a string.

### Private Method: `_generate_section(self, section: Dict, depth: int) -> str`

Recursively generates HTML for a section of the outline, including headings and paragraphs. The depth of the section determines the heading levels (`<h1>`, `<h2>`, etc.).

#### Parameters:
- `section` (Dict): A dictionary representing a section of the book outline.
- `depth` (int): The depth of the section in the hierarchy, used to set heading levels.

#### Returns:
- `str`: HTML content for the section and its subsections.

### Public Method: `save_html(self, output_file_path: str)`

Saves the generated HTML content to a file.

#### Parameters:
- `output_file_path` (str): The path where the HTML file will be saved.

### Example Usage:

```python
# Initialize the generator with the path to the JSON outline file
generator = OutlineHTMLGenerator('path_to_outline.json')

# Generate HTML and save it to a file
generator.save_html('output_outline.html')
```

This class simplifies the process of converting a structured JSON outline into a neatly formatted HTML document, ideal for books or project outlines.

