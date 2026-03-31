import os
import re
import pandas as pd
import io
from fasthtml.common import *
import google.generativeai as genai
from dotenv import load_dotenv
from motor_rag import RAGEngine  # Seu motor de busca em documentos

load_dotenv()

# --- 1. CONFIGURAÇÃO DA IA E ACESSO AO DATA LAKE ---
API_KEY = os.environ.get("CHAVE_DE_API")
genai.configure(api_key=API_KEY)

# Configuração do caminho do Data Lake
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_DATA_LAKE = os.path.join(BASE_DIR, "DataLake")

# Cria a pasta caso ela não exista
if not os.path.exists(PATH_DATA_LAKE):
    os.makedirs(PATH_DATA_LAKE)

# Inicializa o RAG Engine com os documentos do Data Lake
arquivos_pdf = [os.path.join(PATH_DATA_LAKE, f) for f in os.listdir(PATH_DATA_LAKE) if f.endswith('.pdf')]
rag_engine = RAGEngine(pdf_paths=arquivos_pdf) if arquivos_pdf else None

with open("Personalidade.md", "r", encoding="utf-8") as f:
    system_instructions = f.read()

# --- 2. GLOSSÁRIO E ESTILIZAÇÃO CUSTOMIZADA ---
GLOSSARIO = {
    "p-valor": "Probabilidade de o resultado ser ao acaso. < 0,05 indica significância (AGRESTI, 2017).",
    "generalização": "Capacidade de aplicar os dados da amostra para o país todo (CRESWELL, 2014).",
    "significância estatística": "Indica que o padrão nos dados é real e não um erro aleatório.",
}

def destacar_termos(texto):
    for termo in GLOSSARIO.keys():
        # Links em LILÁS (#9C27B0) e em NEGRITO
        subst = f'<a href="#" hx-get="/definicao/{termo}" hx-target="#modal-content" onclick="document.getElementById(\'modal-estatistica\').showModal()" style="color: #9C27B0; font-weight: bold;">{termo}</a>'
        texto = re.sub(f"\\b{termo}\\b", subst, texto, flags=re.IGNORECASE)
    return NotStr(texto)

# CSS para o fundo do Sul Global e bolhas de chat
custom_css = """
body {
    background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                url('https://images.unsplash.com/photo-1501769752-a59efa2298ce?q=80&w=2000'); 
    background-size: cover;
    background-attachment: fixed;
}
#chat-window {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
"""

app, rt = fast_app(hdrs=(picolink, Style(custom_css)))

# --- 3. INTERFACE E ROTAS ---

@rt("/")
def get():
    return Container(
        Header(H1("SOPHIA - Analista de Dados Sênior na Área de Políticas Públicas"), 
               style="text-align: center; margin-top: 2rem; color: #2c3e50;"),
        
        Dialog(Article(Header(B("Dicionário Estatístico")), Div(id="modal-content"),
               Footer(Button("Fechar", onclick="document.getElementById('modal-estatistica').close()", cls="secondary"))),
               id="modal-estatistica"),
        
        Div(id="chat-window", style="height: 55vh; overflow-y: auto; padding: 2rem; margin-bottom: 1.5rem;"),
        
        Form(
            Label("Cérebro da SOPHIA (Modo Gratuito):",
                Select(
                    Option("⚡ Gemini 2.5 Flash (Rápido/Revisão)", value="gemini-2.5-flash"),
                    Option("🧠 Gemini 1.5 Pro (Estatística/Doutorado)", value="gemini-1.5-pro"),
                    name="model_choice"
                )
            ),
            Group(
                Input(name="user_input", placeholder="Consulte o Data Lake ou descreva sua análise..."),
                Input(type="file", name="file_upload", accept=".csv"),
                Button("Enviar")
            ),
            hx_post="/send", hx_target="#chat-window", hx_swap="beforeend",
            enctype="multipart/form-data", onsubmit="this.reset()"
        ),
        P(Small(f"📚 {len(arquivos_pdf)} documentos carregados do Data Lake.")),
        style="max-width: 1000px;"
    )

@rt("/send")
async def post(user_input: str, model_choice: str, file_upload: UploadFile = None):
    # 1. Recuperação de Conhecimento no Data Lake (RAG)
    contexto_rag = ""
    if rag_engine:
        docs_recuperados = rag_engine.recuperar_documentos(user_input)
        contexto_rag = "\n".join([d.page_content for d in docs_recuperados])

    # 2. Processamento de Dados Numéricos (CSV)
    contexto_csv = ""
    if file_upload and file_upload.filename:
        content = await file_upload.read()
        df = pd.read_csv(io.BytesIO(content))
        contexto_csv = f"\nResumo do CSV: {df.describe().to_string()}"

    # 3. Prompt Final Consolidado
    prompt = f"CONTEXTO DO DATA LAKE:\n{contexto_rag}\n\nESTATÍSTICAS:\n{contexto_csv}\n\nPERGUNTA: {user_input}"

    try:
        model = genai.GenerativeModel(model_name=model_choice, system_instruction=system_instructions)
        response = model.start_chat().send_message(prompt)
        
        # Estilização das Badges
        if "pro" in model_choice:
            badge_style = "background: #007bff; color: white;" # Azul Pro
            label = "PRO"
        else:
            badge_style = "background: #FCE4EC; color: #C2185B;" # ROSA CLARO FLASH
            label = "FLASH"

        user_html = Div(B("Você:"), P(user_input), style="background:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:10px;")
        sophia_html = Div(
            B("SOPHIA 🤖"), Span(label, style=f"{badge_style} padding:2px 8px; border-radius:4px; font-size:11px; margin-left:8px;"),
            Div(destacar_termos(response.text)), 
            style="background:#eef6ff; padding:15px; border-left:5px solid #007bff; border-radius:0 10px 10px 0;"
        )
        return Div(user_html, sophia_html, style="margin-bottom: 25px;")
    except Exception as e:
        return Div(P(f"Erro: {str(e)}"), style="color: red;")

@rt("/definicao/{termo}")
def get_definicao(termo: str):
    return P(GLOSSARIO.get(termo.lower(), "Definição não encontrada."))

serve()

