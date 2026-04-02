import os
import re
import pandas as pd
import io
from fasthtml.common import *
from google import genai
from dotenv import load_dotenv
from motor_rag import RAGEngine
from pathlib import Path

load_dotenv()

# --- CONFIGURAÇÃO DA IA E ACESSO AO DATA LAKE ---
API_KEY = os.environ.get("CHAVE_DE_API")
client = genai.Client(api_key=API_KEY)

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

# --- GLOSSÁRIO E ESTILIZAÇÃO CUSTOMIZADA ---
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
    background-color: #FAF8F5;
    background-image: 
        linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
        url('https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=2000&q=80');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
main {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}
#chat-window {
    background: rgba(255, 255, 255, 0.96);
    border-radius: 15px 15px 0 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    backdrop-filter: blur(10px);
    height: 50vh;
    overflow-y: auto;
    padding: 2rem;
    border: 1px solid #ddd;
    border-bottom: none;
}
#chat-input-area {
    background: rgba(255, 255, 255, 0.96);
    border-radius: 0 0 15px 15px;
    padding: 1rem 2rem;
    border: 1px solid #ddd;
    border-top: 2px solid #007bff;
    margin-bottom: 1.5rem;
}
#upload-area {
    background: rgba(255, 255, 255, 0.96);
    border-radius: 10px;
    padding: 1rem;
    border: 1px solid #ddd;
    margin-bottom: 1rem;
}
#file-status {
    backdrop-filter: blur(5px);
}
.container {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(0,123,255,.3);
    border-radius: 50%;
    border-top-color: #007bff;
    animation: spin 1s ease-in-out infinite;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
"""

app, rt = fast_app(hdrs=(picolink, Style(custom_css)), live=True)

# --- INTERFACE E ROTAS ---

@rt("/")
def get():
    return Title("SOPHIA - Analista de Dados"), Main(
        Header(H1("SOPHIA - Analista de Dados Sênior na Área de Políticas Públicas"), 
               style="text-align: center; margin-top: 2rem; color: #2c3e50;"),
        
        Dialog(
            Article(
                Header(B("Dicionário Estatístico")), 
                Div(id="modal-content"),
                Footer(Button("Fechar", onclick="document.getElementById('modal-estatistica').close()", cls="secondary"))
            ),
            id="modal-estatistica"
        ),
        
        # Janela de conversa
        Div(
            P("👋 Olá! Sou a SOPHIA, sua analista de dados sênior.", style="color: #666; text-align: center; margin-top: 1rem;"),
            P("Faça upload de um arquivo ou consulte o Data Lake para começar.", style="color: #999; text-align: center; font-size: 0.9rem;"),
            id="chat-window"
        ),
        
        # Campo de mensagem dentro da área de chat
        Div(
            Div(Span(cls="loading"), Span(" SOPHIA está pensando..."), id="send-loading", cls="htmx-indicator", style="color: #007bff; margin-bottom: 0.5rem;"),
            Form(
                Group(
                    Input(name="user_input", placeholder="Digite sua mensagem para a SOPHIA...", required=True, id="msg-input", style="flex: 1;"),
                    Button("➤ Enviar", type="submit", id="send-btn")
                ),
                hx_post="/send", 
                hx_target="#chat-window", 
                hx_swap="beforeend",
                hx_indicator="#send-loading",
                id="chat-form",
                onsubmit="document.getElementById('send-btn').disabled=true;"
            ),
            id="chat-input-area"
        ),
        
        # Área de upload de arquivo
        Div(
            Button("📎 Anexar arquivo", id="attach-btn", onclick="document.getElementById('file-input').click();", style="width: 100%; margin-bottom: 0.5rem;"),
            Form(
                Input(type="file", name="file_upload", 
                      accept=".csv,.txt,.md,.pdf,.docx,.doc,.xlsx,.xls,.pptx,.ppt,.jpg,.jpeg,.png,.gif,.bmp,.webp,.py,.js,.html,.css,.json,.xml,.yaml,.yml", 
                      id="file-input",
                      style="display: none;",
                      onchange="document.getElementById('file-name').textContent = this.files[0]?.name || 'Nenhum arquivo selecionado'; document.getElementById('open-btn').style.display = this.files[0] ? 'inline-block' : 'none';"),
                Div(
                    Span(id="file-name", style="color: #666; font-size: 0.9rem;"),
                    Button("Abrir", type="submit", id="open-btn", style="display: none; margin-left: 1rem;"),
                    style="margin-bottom: 0.5rem;"
                ),
                hx_post="/upload",
                hx_target="#file-status",
                hx_encoding="multipart/form-data",
                hx_indicator="#upload-loading",
                onsubmit="document.getElementById('open-btn').disabled=true;"
            ),
            Div(
                Div(id="file-status"),
                Div(Span(cls="loading"), Span(" Carregando..."), id="upload-loading", cls="htmx-indicator", style="color: #007bff;")
            ),
            id="upload-area"
        ),
        
        P(Small(f"📚 {len(arquivos_pdf)} documentos carregados no Data Lake.")),
        cls="container",
        style="max-width: 1000px; margin: auto;"
    )

# Variáveis globais para armazenar arquivos carregados
current_file_data = None
current_file_name = None
current_file_type = None

@rt("/upload")
async def post_upload(file_upload: UploadFile):
    global current_file_data, current_file_name, current_file_type
    
    if not file_upload or not hasattr(file_upload, 'filename') or not file_upload.filename:
        return Div(
            P("⚠️ Nenhum arquivo selecionado."),
            Script("document.getElementById('open-btn').disabled=false;"),
            style="color: orange; background: #fff3cd; padding: 10px; border-radius: 5px;"
        )
    
    # Retorna status de carregamento
    try:
        content = await file_upload.read()
        file_extension = Path(file_upload.filename).suffix.lower()
        current_file_name = file_upload.filename
        current_file_type = file_extension
        
        # Processar CSV
        if file_extension == '.csv':
            df = pd.read_csv(io.BytesIO(content))
            current_file_data = f"Resumo Estatístico:\n{df.describe().to_string()}\n\nPrimeiras linhas:\n{df.head(10).to_string()}"
            file_info = f"Linhas: {len(df)} | Colunas: {len(df.columns)}"
        
        # Processar arquivos de texto
        elif file_extension in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.yaml', '.yml']:
            current_file_data = content.decode('utf-8')
            file_info = f"Tamanho: {len(current_file_data)} caracteres"
        
        # Processar documentos Word/Excel
        elif file_extension in ['.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt']:
            current_file_data = content
            file_info = f"Tamanho: {len(content)} bytes"
        
        # Processar PDF
        elif file_extension == '.pdf':
            current_file_data = content
            file_info = f"Tamanho: {len(content)} bytes"
        
        # Processar imagens
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            current_file_data = content
            file_info = f"Tamanho: {len(content)} bytes"
        
        else:
            current_file_data = None
            current_file_name = None
            current_file_type = None
            return Div(
                P(f"⚠️ Formato de arquivo não suportado: {file_extension}"),
                Script("document.getElementById('open-btn').disabled=false;"),
                style="color: orange; background: #fff3cd; padding: 10px; border-radius: 5px;"
            )
        
        return Div(
            P(f"✅ Carregado: {file_upload.filename}"),
            P(Small(f"{file_extension} | {file_info}"), style="color: #666;"),
            Script("document.getElementById('open-btn').disabled=false; document.getElementById('open-btn').style.display='none'; document.getElementById('file-name').textContent='';"),
            style="color: green; background: #d4edda; padding: 10px; border-radius: 5px; margin-top: 0.5rem;"
        )
    except Exception as e:
        current_file_data = None
        current_file_name = None
        current_file_type = None
        return Div(
            P(f"❌ Falha no carregamento: {str(e)}"),
            Script("document.getElementById('open-btn').disabled=false;"),
            style="color: red; background: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 0.5rem;"
        )

@rt("/send")
async def post_send(user_input: str):
    global current_file_data, current_file_name, current_file_type
    
    if not user_input or not user_input.strip():
        return Div(
            P("⚠️ Por favor, digite uma mensagem."), 
            Script("""
                document.getElementById('send-btn').disabled=false;
            """),
            style="color: orange; background: #fff3cd; padding: 10px; border-radius: 5px; margin-bottom: 10px;"
        )
    
    # 1. Recuperação de Conhecimento no Data Lake (RAG)
    contexto_rag = ""
    if rag_engine:
        try:
            docs_recuperados = rag_engine.recuperar_documentos(user_input)
            contexto_rag = "\n".join([d.page_content for d in docs_recuperados])
        except Exception as e:
            contexto_rag = f"Erro ao recuperar documentos: {str(e)}"

    # 2. Preparar conteúdo do arquivo carregado
    file_parts = []
    contexto_arquivo = ""
    
    if current_file_data and current_file_name:
        # Para arquivos de texto e CSV (já processados como string)
        if isinstance(current_file_data, str):
            contexto_arquivo = f"\n\nConteúdo do arquivo '{current_file_name}':\n{current_file_data}"
        
        # Para arquivos binários (PDF, imagens, documentos Office)
        elif isinstance(current_file_data, bytes):
            try:
                # Upload do arquivo para o Gemini
                uploaded_file = client.files.upload(file=io.BytesIO(current_file_data), mime_type=get_mime_type(current_file_type))
                file_parts.append(genai.types.Part.from_uri(file_uri=uploaded_file.uri, mime_type=uploaded_file.mime_type))
                contexto_arquivo = f"\n\nArquivo anexado: '{current_file_name}' (tipo: {current_file_type})"
            except Exception as e:
                contexto_arquivo = f"\n\nErro ao processar arquivo '{current_file_name}': {str(e)}"

    # 3. Prompt Final Consolidado
    prompt_text = f"CONTEXTO DO DATA LAKE:\n{contexto_rag}\n\nARQUIVO ANEXADO:\n{contexto_arquivo}\n\nPERGUNTA: {user_input}"

    try:
        # Se houver arquivos binários, enviar com multimodal
        if file_parts:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt_text] + file_parts,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instructions
                )
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_text,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instructions
                )
            )
        
        user_html = Div(
            B("👤 Você:"), 
            P(user_input), 
            style="background:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:10px;"
        )
        sophia_html = Div(
            Div(
                B("SOPHIA 🤖"), 
                Span("FLASH", style="background: #FCE4EC; color: #C2185B; padding:2px 8px; border-radius:4px; font-size:11px; margin-left:8px;")
            ),
            Div(destacar_termos(response.text)), 
            style="background:#eef6ff; padding:15px; border-left:5px solid #007bff; border-radius:0 10px 10px 0; margin-bottom:20px;"
        )
        return Div(
            user_html, 
            sophia_html,
            Script("""
                document.getElementById('send-btn').disabled=false;
                document.getElementById('msg-input').value='';
                var chatWindow = document.getElementById('chat-window');
                chatWindow.scrollTop = chatWindow.scrollHeight;
            """)
        )
    except Exception as e:
        return Div(
            P(f"❌ Erro ao processar sua solicitação: {str(e)}"), 
            Script("""
                document.getElementById('send-btn').disabled=false;
                document.getElementById('msg-input').value='';
            """),
            style="color: red; background: #ffe6e6; padding: 15px; border-radius: 10px; margin-bottom: 10px;"
        )

def get_mime_type(file_extension):
    """Retorna o MIME type baseado na extensão do arquivo"""
    mime_types = {
        '.pdf': 'application/pdf',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xls': 'application/vnd.ms-excel',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.ppt': 'application/vnd.ms-powerpoint',
    }
    return mime_types.get(file_extension, 'application/octet-stream')

@rt("/definicao/{termo}")
def get_definicao(termo: str):
    return P(GLOSSARIO.get(termo.lower(), "Definição não encontrada."))

if __name__ == "__main__":
    serve()
