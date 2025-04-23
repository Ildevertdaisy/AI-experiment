import logging
import os
from pathlib import Path


import requests
from dotenv import load_dotenv


from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    ApiVlmOptions,
    ResponseFormat,
    VlmPipelineOptions
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline


def ollama_vlm_options(model: str, prompt: str):
    
    options = ApiVlmOptions(
        url = "http://localhost:11434/v1/chat/completions",
        params = dict(
            model = model
        ),
        prompt=prompt,
        timeout=900,
        scale=1.0,
        response_format=ResponseFormat.MARKDOWN
    )

    return options


def main():
    
    logging.basicConfig(level=logging.INFO)

    input_doc_path = Path("./documents/test.pdf")

    pipeline_options = VlmPipelineOptions(
        enable_remote_services=True
    )
    

    prompt = """
- Instrution: OCR the text from the image attached in markdown format. Make sure to only extract only the text and don't forget to consider and detect checkboxex in images."
- Constrain:"
   - Don't forget any text inside the image
   - You only respond with the text extract in markdown.
   - You also respect the table(s) structure(s) mentionned and reflect it in markdown
   - Don't include the ```mardown <text extracted>``` delimiter in your response
   - You also respect the checkmark in checkboxes presented.
   - If there's a checked checbox, represents if with this character: ☑️
   - If there's an unchecked checbox, represents if with this character: ☐
""" 
# To be defined later


    pipeline_options.vlm_options = ollama_vlm_options(
        model="llama3.2-vision",
        prompt="OCR the full page to markdown"
    )


    # Create the DocumentConverter and launh the conversion.
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                pipeline_cls=VlmPipeline
            )
        }
    )


    result = doc_converter.convert(input_doc_path)
    print(result.document.export_to_markdown())


if __name__ == "__main__":
    main()