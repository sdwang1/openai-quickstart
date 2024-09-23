from typing import Optional
from model import Model
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from utils import LOG
import json
import time

class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()


    def translate_pdf(self, input_file_path: str, source_language: str = "Auto", target_language: str = "Chinese", output_file_format: str = "markdown", pages: Optional[int] = None):
        self.book = self.pdf_parser.parse_pdf(input_file_path, pages)

        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                time.sleep(3)
                prompt_messages = self.model.translate_prompt(content, target_language)
                LOG.debug(prompt_messages)
                translation, status = self.model.make_request(prompt_messages)
                LOG.info(translation)

                translation_obj = translation
                try:
                    translation_obj = json.loads(translation)
                    # Update the content in self.book.pages directly
                    self.book.pages[page_idx].contents[content_idx].set_translation(translation_obj['translation'], status)
                except ValueError:
                    pass

        return self.writer.save_translated_book(self.book, output_file_format)
