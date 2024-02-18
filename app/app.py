
import os
import gradio as gr
from dotenv import load_dotenv,find_dotenv
from rag.assistant import Assistant


# load environment variables
_ =load_dotenv(find_dotenv(".env"))

PDF_PATH= os.environ["PDF_PATH"]
FAISS_INDEX_PATH= os.environ["FAISS_INDEX_PATH"]
UI_PORT: int = int(os.getenv("UI_PORT", "8046"))

# load assistant
qa_assistant = Assistant(pdf_path=PDF_PATH, index_path=FAISS_INDEX_PATH)


def respond(question, history):
    response = qa_assistant.request(question)
    return response

# Define UI
PLACE_HOLDER = "¡Hola!, ¿En que te puedo ayudar?"
BOTH_ICON = "assets/bot.png"
USER_ICON = "assets/user.png"
chatbot = gr.ChatInterface(
    fn=respond,
    chatbot=gr.Chatbot(elem_id="chatbot", height="auto", avatar_images=[USER_ICON, BOTH_ICON]),
    title="",
    textbox=gr.Textbox(placeholder=PLACE_HOLDER, container=False, scale=7),
    clear_btn="Limpiar",
    retry_btn=None,
    undo_btn=None,
    submit_btn="Enviar",
    theme=gr.themes.Default(primary_hue="purple", secondary_hue="indigo"),
)

if __name__ == "__main__":
    chatbot.launch(server_name="0.0.0.0", server_port=UI_PORT)
