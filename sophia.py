import os
import gradio as gr
from google import genai
from dotenv import load_dotenv
from google.genai import types
from motor_rag import RAGEngine

load_dotenv()

api_key = os.environ.get("CHAVE_DE_API")

client = genai.Client(api_key=api_key)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVOS_PDF = [
    os.path.join(BASE_DIR, "documentos", "L8213consol.pdf"),
]

rag_engine = None

with open("Personalidade.md", "r", encoding="utf-8") as f:
    system_instructions = f.read()

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instructions,
        temperature=1.7,
        top_p=0.9,
        top_k=50,
        max_output_tokens=2048,
    )
)


def _obter_rag_engine() -> RAGEngine:
    global rag_engine
    if rag_engine is None:
        rag_engine = RAGEngine(pdf_paths=ARQUIVOS_PDF)
    return rag_engine


def consultar_documentacao(pergunta: str) -> str:
    docs = _obter_rag_engine().recuperar_documentos(pergunta)
    if not docs:
        return "Nenhuma informação relevante encontrada nos documentos."
    return "\n\n".join([doc.page_content for doc in docs])


def _detalhar_erro(ex: Exception) -> str:
    folhas = []

    def _coletar_folhas(err):
        if hasattr(err, "exceptions") and getattr(err, "exceptions"):
            for sub in err.exceptions:
                _coletar_folhas(sub)
        else:
            folhas.append(f"{type(err).__name__}: {err}")

    _coletar_folhas(ex)

    if folhas:
        return f"{type(ex).__name__}: {ex} | Causas folha: {' | '.join(folhas)}"

    return f"{type(ex).__name__}: {ex}"


def generate_response(user_message, chat_history):
    try:
        contexto_encontrado = consultar_documentacao(user_message)
        mensagem_com_contexto = f"""

        Mensagem do usuário:
        {user_message}
        
        Contexto relevante:        
        {contexto_encontrado}

        Responda à mensagem do usuário utilizando o contexto encontrado, se necessário.
        """

        response = chat.send_message(mensagem_com_contexto)
        return response.text
    except Exception as e:
        return f"Ocorreu um erro: {_detalhar_erro(e)}"


demo = gr.ChatInterface(
    fn=generate_response,
    title="Sophia - Analista de Dados",
    description="Converse com a Sophia diretamente pelo navegador."
)

if __name__ == "__main__":
    server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    demo.launch(server_name=server_name, server_port=server_port)
