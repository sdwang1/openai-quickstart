import sys
import os
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, LOG
from model import OpenAIModel
from translator import PDFTranslator, TranslationConfig

def translation(input_file, source_language, target_language):
    LOG.debug(
        f"[PDF 翻译工具]\n输入的文件: {input_file.name}\n源语言: {source_language}\n目标语言: {target_language}"
    )
    # return None
    output_file_path = Translator.translate_pdf(
        input_file.name,
        source_language=source_language,
        target_language=target_language
    )

    return output_file_path

def launch_gradio():
    with gr.Blocks() as demo:
        input_file = gr.File(
            label="请上传 PDF文件", file_count='single', file_types=['.pdf']
        )
        source_language = gr.Textbox(
            label="源语言（默认: 检测语言）", placeholder="Auto", value="Auto"
        )
        target_language = gr.Textbox(
            label="目标语言（默认: 中文）", placeholder="Chinese", value="Chinese"
        )
        output_file = gr.File(label="下载翻译结果文件(.md)")

        gr.ClearButton(
            components=[
                input_file,
                source_language,
                target_language
            ]
        )
        submit = gr.Button("Submit")
        submit.click(
            translation,
            inputs=[
                input_file,
                source_language,
                target_language
            ],
            outputs=[output_file],
        )

    demo.launch(share=True, server_name="0.0.0.0")

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    config = TranslationConfig()
    config.initialize(args)
    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    model = OpenAIModel(model=model_name)

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    global Translator
    Translator = PDFTranslator(model)
    launch_gradio()