import openai
from typing import List, Dict
import os
import json
import tiktoken
import re
from ebooklib import epub
import html
from abc import ABC, abstractmethod
#from gpt4all import GPT4All
import sys
from PIL import Image, ImageDraw, ImageFont
import io
import base64

#MAX_TOKENS_GPT4ALL = 900
#MAX_CONTEXT_GPT4ALL = 64000
#MODEL_LOCATIONS = "/Users/alexiskirke/Library/Application Support/nomic.ai/GPT4All/"
#models = {"nous":"nous-hermes-llama2-13b.Q4_0.gguf", "meta-128k":"Meta-Llama-3.1-8B-Instruct-128k-Q4_0.gguf","meta-instruct":"Meta-Llama-3-8B-Instruct.Q4_0.gguf"}

class LLMClient(ABC):
    """
    Abstract base class for language model clients.
    """
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """
        Generate text based on the given prompt.

        Args:
            prompt (str): The input prompt for text generation.

        Returns:
            str: The generated text.
        """
        pass

class OpenAIClient(LLMClient):
    """
    Client for interacting with OpenAI's language models.
    """
    def __init__(self, openai_api_key: str="", model: str="gpt-4o-mini"):
        """
        Initialize the OpenAI client.

        Raises:
            ValueError: If the OPENAI_API_KEY environment variable is not set.
        """
        self.model = model
        if not openai_api_key:
            self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            if not self.client.api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
        else:
            self.client = openai.OpenAI(api_key=openai_api_key)

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using OpenAI's language model.

        Args:
            prompt (str): The input prompt for text generation.

        Returns:
            str: The generated text.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

# class GPT4AllClient(LLMClient):
#     """
#     Client for interacting with GPT4All language models.
#     """
#     def __init__(self, model_name: str = "Meta-Llama-3.1-8B-Instruct-128k-Q4_0.gguf",
#                  model_locations=MODEL_LOCATIONS):
#         """
#         Initialize the GPT4All client.

#         Args:
#             model_name (str): The name of the GPT4All model to use.
#         """
#         model_path = os.path.join(model_locations, model_name)
#         self.model = GPT4All(model_path, device='gpu', n_ctx=MAX_CONTEXT_GPT4ALL)

#     def generate_text(self, prompt: str, max_tokens: int = MAX_TOKENS_GPT4ALL) -> str:
#         """
#         Generate text using the GPT4All model.

#         Args:
#             prompt (str): The input prompt for text generation.
#             max_tokens (int): The maximum number of tokens to generate.

#         Returns:
#             str: The generated text.
#         """
#         response = self.model.generate(prompt, max_tokens=max_tokens)
#         return response

class OutlineHTMLGenerator:
    """
    Generator for creating HTML representations of book outlines.
    """
    def __init__(self, json_file_path: str):
        """
        Initialize the OutlineHTMLGenerator.

        Args:
            json_file_path (str): Path to the JSON file containing the outline data.
        """
        self.json_file_path = json_file_path
        self.outline_data = self._load_json()
        self.phrases_to_avoid = ['delves',
        'showcasing',
        'underscores',
        'potential',
        'findings',
        'emerged',
        'invaluable',
        'groundbreaking',
        'relentless',
        'insights',
        'enlightening',
        'explores',
        'demonstrates',
        'highlights',
        'parameters',
        'comprehensive',
        'crucial',
        'intricate',
        'pivotal',
        "In conclusion", 
        "It is important to note", 
        "As mentioned earlier", 
        "This suggests that", 
        "Moreover", 
        "Furthermore", 
        "On the other hand", 
        "In other words", 
        "Therefore", 
        "Additionally", 
        "For instance", 
        "For example", 
        "Consequently", 
        "In summary", 
        "As a result", 
        "It can be seen that", 
        "Another important point", 
        "This means that", 
        "It should be noted that", 
        "One possible explanation", 
        "In essence", 
        "It is clear that", 
        "In fact",
        "It is worth mentioning that", 
        "It is commonly understood that", 
        "To sum up",
        "Generally speaking", 
        "In general", 
        "On the contrary", 
        "Overall"]

    def _load_json(self) -> Dict:
        """
        Load the JSON file containing the outline data.

        Returns:
            Dict: The loaded outline data.
        """
        with open(self.json_file_path, 'r') as file:
            return json.load(file)

    def generate_html(self) -> str:
        """
        Generate the HTML content for the book outline.

        Returns:
            str: The generated HTML content.
        """
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Book Outline</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #2c3e50; }
                h2 { color: #34495e; }
                h3 { color: #7f8c8d; }
                h4 { color: #95a5a6; }
                .paragraph { margin-left: 20px; }
            </style>
        </head>
        <body>
            <h1>Book Outline</h1>
        """

        html_content += self._generate_section(self.outline_data, 1)

        html_content += """
        </body>
        </html>
        """

        return html_content
    
    def _generate_section(self, section: Dict, depth: int) -> str:
        """
        Generate HTML content for a section of the outline.

        Args:
            section (Dict): The section data.
            depth (int): The depth of the section in the outline hierarchy.

        Returns:
            str: The generated HTML content for the section.
        """
        content = ""
        for title, subsections in section.items():
            cleaned_title = title.lstrip('-').strip('"')
            content += f"<h{depth}>{html.escape(cleaned_title)}</h{depth}>\n"
            if isinstance(subsections, dict):
                if "paragraphs" in subsections:
                    for paragraph in subsections["paragraphs"]:
                        content += f'<p class="paragraph">{html.escape(paragraph)}</p>\n'
                else:
                    content += self._generate_section(subsections, depth + 1)
            elif isinstance(subsections, str):
                content += f'<p class="paragraph">{html.escape(subsections)}</p>\n'
        return content

    def save_html(self, output_file_path: str):
        """
        Save the generated HTML content to a file.

        Args:
            output_file_path (str): The path where the HTML file will be saved.
        """
        html_content = self.generate_html()
        with open(output_file_path, 'w') as file:
            file.write(html_content)
        print(f"HTML outline saved to {output_file_path}")

class OutlineEbookGenerator:
    """
    Generator for creating ebooks from book outlines.
    """
    def __init__(self, json_file_path: str, book_title: str = 'Book Outline', book_author: str = 'Outline Generator', generate_cover: bool = False, force_kindle_compatibility: bool = False, override_image_prompt: str = '', openai_api_key: str = "", model: str="gpt-4o-mini"):
        """
        Initialize the OutlineEbookGenerator.

        Args:
            json_file_path (str): Path to the JSON file containing the outline data.
            book_title (str): Title of the book.
            book_author (str): Author of the book.
            generate_cover (bool): Whether to generate a cover image.
            force_kindle_compatibility (bool): Whether to force Kindle compatibility.
            override_image_prompt (str): Custom prompt for cover image generation.
            openai_api_key (str): OpenAI API key
            model (str): gpt-4o-mini or gpt-4o
        """
        self.json_file_path = json_file_path
        self.model = model
        self.outline_data = self._load_json()
        self.book_title = book_title
        self.book_author = book_author
        self.generate_cover = generate_cover
        self.force_kindle_compatibility = force_kindle_compatibility
        self.override_image_prompt = override_image_prompt
        if self.generate_cover:
            self.openai_client = OpenAIClient(openai_api_key=openai_api_key,
                                              model=self.model)

    def _load_json(self) -> Dict:
        """
        Load the JSON file containing the outline data.

        Returns:
            Dict: The loaded outline data.
        """
        with open(self.json_file_path, 'r') as file:
            return json.load(file)

    def generate_ebook(self) -> epub.EpubBook:
        """
        Generate the ebook from the outline data.

        Returns:
            epub.EpubBook: The generated ebook.
        """
        book = epub.EpubBook()
        book.set_identifier('book_outline_' + str(hash(json.dumps(self.outline_data))))
        book.set_title(self.book_title)
        book.set_language('en')
        book.add_author(self.book_author)

        spine = ['nav']
        toc = []

        # Create cover page if requested
        if self.generate_cover:
            cover_image = self._generate_cover_image()
            book.set_cover("cover.jpg", cover_image)

        # Create title page
        title_page = epub.EpubHtml(title='Title Page', file_name='title.xhtml')
        title_page.content = f'''
            <html>
            <head>
                <title>{html.escape(self.book_title)}</title>
            </head>
            <body>
                <h1 style="text-align: center;">{html.escape(self.book_title)}</h1>
                <p style="text-align: center;">{html.escape(self.book_author)}</p>
            </body>
            </html>
        '''
        book.add_item(title_page)
        spine.append(title_page)

        # Create table of contents
        toc_page = epub.EpubHtml(title='Table of Contents', file_name='toc.xhtml')
        toc_content = '<h1>Table of Contents</h1><nav epub:type="toc"><ol>'

        # Generate chapters
        for chapter_num, (chapter_title, chapter_content) in enumerate(self.outline_data.items(), 1):
            cleaned_chapter_title = chapter_title.strip().lstrip('-').replace('"', '')
            chapter = epub.EpubHtml(title=cleaned_chapter_title, file_name=f'chap_{chapter_num}.xhtml')
            chapter.content = f'<h1 id="{self._generate_id(cleaned_chapter_title)}">{html.escape(cleaned_chapter_title)}</h1>'
            chapter.content += self._generate_section(chapter_content, 2, chapter_num)
            
            book.add_item(chapter)
            spine.append(chapter)
            toc.append(chapter)

            # Add chapter to table of contents
            toc_content += f'<li><a href="chap_{chapter_num}.xhtml#{self._generate_id(cleaned_chapter_title)}">{html.escape(cleaned_chapter_title)}</a>'
            if isinstance(chapter_content, dict):
                toc_content += self._generate_toc_section(chapter_content, chapter_num, 2)
            toc_content += '</li>'

        toc_content += '</ol></nav>'
        toc_page.content = toc_content
        book.add_item(toc_page)
        spine.insert(2, toc_page)  # Insert TOC after cover and title page, before chapters

        book.spine = spine
        book.toc = toc
        book.add_item(epub.EpubNcx())
        if self.force_kindle_compatibility:
            book.add_item(epub.EpubNav())

        return book

    def _generate_section(self, section: Dict, depth: int, chapter_num: int) -> str:
        """
        Generate HTML content for a section of the ebook.

        Args:
            section (Dict): The section data.
            depth (int): The depth of the section in the outline hierarchy.
            chapter_num (int): The chapter number.

        Returns:
            str: The generated HTML content for the section.
        """
        content = ""
        for title, subsections in section.items():
            cleaned_title = title.lstrip('-').replace('"', '')
            if depth <= 3:  # Only include h1, h2, and h3
                content += f'<h{depth} id="{self._generate_id(cleaned_title)}">{html.escape(cleaned_title)}</h{depth}>'
            if isinstance(subsections, dict):
                if "paragraphs" in subsections:
                    for paragraph in subsections["paragraphs"]:
                        content += self._process_paragraph(paragraph)
                else:
                    content += self._generate_section(subsections, depth + 1, chapter_num)
            elif isinstance(subsections, str):
                content += self._process_paragraph(subsections)
        return content

    def _generate_toc_section(self, section: Dict, chapter_num: int, depth: int) -> str:
        """
        Generate HTML content for a section of the table of contents.

        Args:
            section (Dict): The section data.
            chapter_num (int): The chapter number.
            depth (int): The depth of the section in the outline hierarchy.

        Returns:
            str: The generated HTML content for the table of contents section.
        """
        content = "<ol>"
        for title, subsections in section.items():
            cleaned_title = title.lstrip('-').replace('"', '')
            content += f'<li><a href="chap_{chapter_num}.xhtml#{self._generate_id(cleaned_title)}">{html.escape(cleaned_title)}</a>'
            if isinstance(subsections, dict) and "paragraphs" not in subsections and depth < 3:
                content += self._generate_toc_section(subsections, chapter_num, depth + 1)
            content += '</li>'
        content += "</ol>"
        return content

    def _generate_id(self, title: str) -> str:
        """
        Generate a valid HTML id from a title.

        Args:
            title (str): The title to convert.

        Returns:
            str: The generated HTML id.
        """
        return re.sub(r'\W+', '-', title.lower())

    def _process_paragraph(self, paragraph: str) -> str:
        """
        Process a paragraph, converting LaTeX equations to MathML.

        Args:
            paragraph (str): The paragraph to process.

        Returns:
            str: The processed paragraph with LaTeX equations converted to MathML.
        """
        # Replace inline LaTeX equations with MathML
        paragraph = re.sub(r'\$(.+?)\$', lambda m: self._latex_to_mathml(m.group(1)), paragraph)
        return f'<p>{html.escape(paragraph)}</p>'

    def _latex_to_mathml(self, latex: str) -> str:
        """
        Convert LaTeX to MathML.

        Args:
            latex (str): The LaTeX equation to convert.

        Returns:
            str: The converted MathML.
        """
        # This is a placeholder function. You would need to implement or use a library
        # that converts LaTeX to MathML. For example, you could use the latex2mathml library.
        # Here's a simple example (you'd need to install latex2mathml first):
        from latex2mathml.converter import convert
        return convert(latex)
        
        # For now, we'll just wrap it in a math tag
        return f'<math xmlns="http://www.w3.org/1998/Math/MathML"><mtext>{html.escape(latex)}</mtext></math>'
    
    def _generate_cover_image(self) -> bytes:
        """
        Generate a cover image for the ebook.

        Returns:
            bytes: The generated cover image data.

        Raises:
            RuntimeError: If the OpenAI API call fails.
        """
        if self.override_image_prompt:
            prompt = self.override_image_prompt
        else:
            prompt = f"Create an image inspired by the words: '{self.book_title}'. The image should have a clear point of focus. It should be photorealistic."
        try:
            response = self.openai_client.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792",
                quality="standard",
                n=1,
            )
        except Exception as e:
            msg = f"Error: _generate_cover_image - OpenAI API call failed: {str(e)}"
            raise RuntimeError(msg) from e

        image_url = response.data[0].url
        
        # Use requests to download the image
        import requests
        image_response = requests.get(image_url)
        
        # Save the image
        image_path = f"{self.book_title}_cover_image.jpg"
        with open(image_path, "wb") as f:
            f.write(image_response.content)
        
        with open(image_path, "rb") as f:
            image_data = f.read()

            # Open the image using PIL
            img = Image.open(io.BytesIO(image_data))
        
        # Create a drawing object
        draw = ImageDraw.Draw(img)

        # chop the image so it is ratio 1.5:1
        width, height = img.size
        target_ratio = 1/1.5
        current_ratio = width / height

        if current_ratio > target_ratio:
            # Image is too wide, crop width
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            img = img.crop((left, 0, left + new_width, height))
        elif current_ratio < target_ratio:
            # Image is too tall, crop height
            new_height = int(width / target_ratio)
            top = (height - new_height) // 2
            img = img.crop((0, top, width, top + new_height))

        # Convert the image to RGB mode
        img = img.convert('RGB')
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()

    def save_ebook(self, output_file_path: str):
        """
        Save the generated ebook to a file.

        Args:
            output_file_path (str): The path where the ebook will be saved.
        """
        book = self.generate_ebook()
        epub.write_epub(output_file_path, book, {})
        print(f"Ebook-compatible outline saved to {output_file_path}")


class BookOutlineGenerator:
    """
    Generator for creating book outlines.
    """
    #def __init__(self, working_dir: str = 'outline_steps', use_gpt4all: bool = False, openai_api_key: str = ""):
    def __init__(self, working_dir: str = 'outline_steps', openai_api_key: str = ""):
        use_gpt4all = False
        """
        Initialize the BookOutlineGenerator.

        Args:
            working_dir (str): The working directory for saving outline steps.
            use_gpt4all (bool): (REMOVED TEMPORARILY) Whether to use GPT4All instead of OpenAI.
        """
        self.phrases_to_avoid = ['delves',
        'showcasing',
        'underscores',
        'potential',
        'findings',
        'emerged',
        'invaluable',
        'groundbreaking',
        'relentless',
        'insights',
        'enlightening',
        'explores',
        'demonstrates',
        'highlights',
        'parameters',
        'comprehensive',
        'crucial',
        'intricate',
        'pivotal',
        "In conclusion", 
        "It is important to note", 
        "As mentioned earlier", 
        "This suggests that", 
        "Moreover", 
        "Furthermore", 
        "On the other hand", 
        "In other words", 
        "Therefore", 
        "Additionally", 
        "For instance", 
        "For example", 
        "Consequently", 
        "In summary", 
        "As a result", 
        "It can be seen that", 
        "Another important point", 
        "This means that", 
        "It should be noted that", 
        "One possible explanation", 
        "In essence", 
        "It is clear that", 
        "In fact",
        "It is worth mentioning that", 
        "It is commonly understood that", 
        "To sum up",
        "Generally speaking", 
        "In general", 
        "On the contrary", 
        "Overall"]
        self.working_dir = working_dir
        os.makedirs(self.working_dir, exist_ok=True)
        self.full_outline = {}
        self.cumulative_tokens_sent = 0
        self.cumulative_tokens_received = 0
        self.encoder = tiktoken.encoding_for_model("gpt-4o")
        self.total_sections = 0
        self.completed_sections = 0
        #self.use_gpt4all = use_gpt4all
        
        if use_gpt4all:
            #self.llm_client = GPT4AllClient()
            pass
        else:
            self.llm_client = OpenAIClient(openai_api_key=openai_api_key)

    def send_prompt(self, topic: str, num_chapters: int = 3, sections_per_chapter: int = 3, subsections_per_section: int = 3, paras_per_subsection: int = 1, paragraph_style: str = '') -> Dict:
        """
        Generate a complete book outline based on the given parameters.

        Args:
            topic (str): The main topic of the book.
            num_chapters (int): Number of chapters to generate.
            sections_per_chapter (int): Number of sections per chapter.
            subsections_per_section (int): Number of subsections per section.
            paras_per_subsection (int): Number of paragraphs per subsection.
            paragraph_style (str): Style guide for paragraph generation.

        Returns:
            Dict: The complete book outline.
        """
        print("Starting outline generation...")
        self.full_outline = {topic: {}}
        self._generate_chapters(topic, num_chapters)
        self._generate_level1(sections_per_chapter)
        self._generate_level2(subsections_per_section)
        self._generate_level3(paras_per_subsection, paragraph_style)
        print("Outline generation complete.")
        print(f"Cumulative tokens sent: {self.cumulative_tokens_sent}")
        print(f"Cumulative tokens received: {self.cumulative_tokens_received}")
        return self.full_outline

    def _generate_chapters(self, topic: str, num_chapters: int):
        """
        Generate chapter titles for the book outline.

        Args:
            topic (str): The main topic of the book.
            num_chapters (int): Number of chapters to generate.
        """
        print(f"Generating {num_chapters} chapters for topic: {topic}")
        prompt = f"Generate {num_chapters} chapter titles for a book about {topic}. Insure each title begins with the word Chapter and the chapter number, e.g. 'Chapter 1: ...'"
        response = self._send_request(prompt, is_title=True)
        chapters = response.strip().split('\n')
        self.full_outline[topic] = {chapter.strip(): {} for chapter in chapters[:num_chapters]}
        
        # Save chapters to file
        with open(os.path.join(self.working_dir, 'outline_depth_0.json'), 'w') as f:
            json.dump(self.full_outline, f, indent=2)
        
        print("Chapter generation complete.")

    def _generate_level1(self, sections_per_chapter: int):
        """
        Generate level 1 sections for each chapter.

        Args:
            sections_per_chapter (int): Number of sections to generate per chapter.
        """
        print(f"Generating level 1 sections")
        for chapter_title in self.full_outline[list(self.full_outline.keys())[0]]:
            context = self._get_outline_context()
            prompt = f"Given the following outline context:\n\n{context}\n\nGenerate {sections_per_chapter} section titles for the chapter titled: {chapter_title}, in such as a way as to avoid repeating material in earlier or later chapters or sections. Do not include the word 'Section' or a section number in the section titles."
            response = self._send_request(prompt, is_title=True)
            sections = response.strip().split('\n')
            self.full_outline[list(self.full_outline.keys())[0]][chapter_title] = {section.strip(): {} for section in sections[:sections_per_chapter]}
        
        # Save level 1 to file
        with open(os.path.join(self.working_dir, 'outline_depth_1.json'), 'w') as f:
            json.dump(self.full_outline, f, indent=2)
        
        print("Level 1 section generation complete.")

    def _generate_level2(self, subsections_per_section: int):
        """
        Generate level 2 subsections for each section.

        Args:
            subsections_per_section (int): Number of subsections to generate per section.
        """
        print(f"Generating level 2 sections")
        for chapter_title, chapter_content in self.full_outline[list(self.full_outline.keys())[0]].items():
            for section_title in chapter_content:
                context = self._get_outline_context()
                prompt = f"Given the following outline context:\n\n{context}\n\nGenerate {subsections_per_section} subsection titles for the section titled: {section_title}, in such as a way as to avoid repeating material in earlier pr later chapters or sections. Do not include the word 'subsection' or a subsection number in the subsection titles."
                response = self._send_request(prompt, is_title=True)
                subsections = response.strip().split('\n')
                self.full_outline[list(self.full_outline.keys())[0]][chapter_title][section_title] = {subsection.strip(): {} for subsection in subsections[:subsections_per_section]}
        
        # Save level 2 to file
        with open(os.path.join(self.working_dir, 'outline_depth_2.json'), 'w') as f:
            json.dump(self.full_outline, f, indent=2)
        
        print("Level 2 section generation complete.")

    def _generate_level3(self, paras_per_subsection: int, paragraph_style: str):
        """
        Generate level 3 paragraphs for each subsection.

        Args:
            paras_per_subsection (int): Number of paragraphs to generate per subsection.
            paragraph_style (str): Style guide for paragraph generation.
        """
        print(f"Generating level 3 sections with paragraphs")
        self._count_total_sections(self.full_outline)  # Count total sections before starting
        for chapter_title, chapter_content in self.full_outline[list(self.full_outline.keys())[0]].items():
            for section_title, section_content in chapter_content.items():
                for subsection_title in section_content:
                    context = self._get_outline_context()
                    prompt = f"You are a professional author.  Do not use any of the phrases or words in this list: \n{self.phrases_to_avoid}.\n Given the following outline context:\n\n{context}\n\nWrite {paras_per_subsection} paragraphs about this topic: '{subsection_title}' (which you are an expert on), in such as a way as to avoid repeating concepts covered in earlier or future chapters or sections or paragraphs. Do not use any of the phrases or words in this list: {self.phrases_to_avoid}. \n" + paragraph_style
                    response = self._send_request(prompt, is_title=False)
                    paragraphs = response.strip().split('\n\n')
                    self.full_outline[list(self.full_outline.keys())[0]][chapter_title][section_title][subsection_title] = {'paragraphs': paragraphs[:paras_per_subsection]}
                    
                    # Update progress
                    self.completed_sections += 1
                    self._print_progress()
        
        # Save level 3 to file
        with open(os.path.join(self.working_dir, 'outline_depth_3.json'), 'w') as f:
            json.dump(self.full_outline, f, indent=2)
        
        print("Level 3 section generation with paragraphs complete.")

    def _send_request(self, prompt: str, is_title: bool):
        """
        Send a request to the language model and process the response.

        Args:
            prompt (str): The prompt to send to the language model.
            is_title (bool): Whether the request is for generating titles.

        Returns:
            str: The generated text from the language model.
        """
        tokens_sent = len(self.encoder.encode(prompt))
        self.cumulative_tokens_sent += tokens_sent
        prompt += "\nOnly respond with the content requested, no introduction or commentary."
        
        # if self.use_gpt4all and is_title:
        #     response = self.llm_client.generate_text(prompt, max_tokens=200)
        # else:
        response = self.llm_client.generate_text(prompt)
        
        tokens_received = len(self.encoder.encode(response))
        self.cumulative_tokens_received += tokens_received
        
        print(f"Cumulative tokens sent: {self.cumulative_tokens_sent}, Cumulative tokens received: {self.cumulative_tokens_received}")
        return response

    def _get_outline_context(self) -> str:
        """
        Get the current outline context as a JSON string.

        Returns:
            str: The current outline context as a JSON string.
        """
        return json.dumps(self.full_outline, indent=2)

    def _print_progress(self):
        """
        Print the current progress of outline generation.
        """
        percentage = (self.completed_sections / self.total_sections) * 100
        print(f"Progress: {percentage:.2f}% complete ({self.completed_sections}/{self.total_sections} sections)")

    def _count_total_sections(self, outline: Dict):
        self.total_sections = 0  # Reset the count
        for _, content in outline.items():
            if isinstance(content, dict):
                self._count_total_sections_recursive(content)

    def _count_total_sections_recursive(self, content: Dict):
        for _, subcontent in content.items():
            self.total_sections += 1
            if isinstance(subcontent, dict) and 'paragraphs' not in subcontent:
                self._count_total_sections_recursive(subcontent)

class BookWriter:
    # def __init__(self, title: str, use_gpt4all: bool = False, working_dir: str = 'outline_steps', openai_api_key: str=""):
    def __init__(self, title: str, working_dir: str = 'outline_steps', openai_api_key: str="", model: str="gpt-4o-mini"):
        self.title = title
        self.model = model
        print(f"Using model {model}")
        self.openai_api_key = openai_api_key
        #self.generator = BookOutlineGenerator(use_gpt4all=use_gpt4all, working_dir=working_dir, openai_api_key=self.openai_api_key)
        self.generator = BookOutlineGenerator(working_dir=working_dir, openai_api_key=self.openai_api_key)
        self.outline = None
        self.paragraph_style = """Write in a short snappy and modern style, but not too conversational. Write in shorter sentences, and avoid adjectives and adverbs. Sound like a human, not a Large Language Model. Include examples occasionally. Include stories occasionally. If they are not true, say that they are illustrative. But you can include true stories as well."""
        

    def generate_outline(self, num_chapters: int = 3, sections_per_chapter: int = 2, subsections_per_section: int = 3, paras_per_subsection: int = 3):
        self.outline = self.generator.send_prompt(
            self.title, 
            num_chapters=num_chapters, 
            sections_per_chapter=sections_per_chapter, 
            subsections_per_section=subsections_per_section, 
            paras_per_subsection=paras_per_subsection, 
            paragraph_style=self.paragraph_style
        )
        print("Book outline generation complete.")
        return self.outline

    def generate_ebook(self, author: str = 'Book Writer', generate_cover: bool = True, force_kindle_compatibility: bool = True, image_prompt: str = ''):
        if not self.outline:
            raise ValueError("Outline has not been generated yet. Call generate_outline() first.")

        filename = 'outline_depth_3.json'
        filename = os.path.join(self.generator.working_dir, filename)
        
        ebook_generator = OutlineEbookGenerator(
            filename, 
            book_title=self.title, 
            book_author=author, 
            generate_cover=generate_cover, 
            force_kindle_compatibility=force_kindle_compatibility, 
            override_image_prompt=image_prompt,
            openai_api_key=self.openai_api_key,
            model = self.model
        )
        
        output_filename = f"{self.title[:30]}.epub"
        ebook_generator.save_ebook(output_filename)
        print(f"Ebook generated and saved as {output_filename}")
