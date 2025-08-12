import gradio as gr
from pinecone import Pinecone
import os
from dotenv import load_dotenv, find_dotenv
from transformers import AutoProcessor, AutoModel
import torch

load_dotenv(find_dotenv())

from src.retrievers.default import DefaultRetriever

retriever = DefaultRetriever({})

retriever.process()

# # 处理用户输入并展示检索结果
# def display_results(input_text, input_image):
#     # 调用检索组件
#     results = search_with_text(input_text)

#     # 构建HTML输出，用于展示图片和文本
#     output_html = "<div style='display: flex; flex-wrap: wrap; gap: 20px;'>"
#     for result in results:
#         output_html += f"""
#         <div style='border: 1px solid #ccc; padding: 10px;'>
#             <p>{result["chunk_text"]} ({result["score"]})</p>
#         </div>
#         """
#     output_html += "</div>"
#     return output_html


# # 创建Gradio界面
# with gr.Blocks() as demo:
#     gr.Markdown("# RAG Retrieval Component UI")

#     # 输入区域
#     with gr.Column():
#         text_input = gr.Textbox(
#             label="Input Text", placeholder="Enter your query text..."
#         )
#         image_input = gr.Image(label="Input Image", type="pil")

#     # 提交按钮
#     submit_button = gr.Button("Retrieve")

#     # 输出区域（使用HTML组件展示图片和文本）
#     output = gr.HTML(label="Retrieved Results")

#     # 绑定按钮点击事件
#     submit_button.click(
#         fn=display_results, inputs=[text_input, image_input], outputs=output
#     )

# # 启动Gradio应用
# demo.launch(debug=True)
