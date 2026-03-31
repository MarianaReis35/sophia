import os
import sys
from contextlib import redirect_stderr, redirect_stdout
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def _log_stderr(msg: str) -> None:
    try:
        print(msg, file=sys.stderr)
    except OSError:
        # Em algumas execucoes via MCP stdio o stderr pode estar indisponivel.
        pass


def _garantir_stderr_disponivel() -> None:
    try:
        sys.stderr.flush()
    except Exception:
        # O tqdm/transformers usa stderr para barra de progresso.
        # Se o descritor estiver invalido no subprocesso MCP, redirecionamos para devnull.
        sys.stderr = open(os.devnull, "w", encoding="utf-8")


class RAGEngine:
    def __init__(self, pdf_paths):
        _garantir_stderr_disponivel()
        os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
        os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

        docs = []
        for path in pdf_paths:
            if os.path.exists(path):
                loader = PyPDFLoader(path)
                docs.extend(loader.load())
            else:
                _log_stderr(f"Aviso: Arquivo {path} não encontrado.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        with open(os.devnull, "w", encoding="utf-8") as null_stream:
            with redirect_stdout(null_stream), redirect_stderr(null_stream):
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )

        self.vector_store = FAISS.from_documents(
            documents=splits, embedding=embeddings)

        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        _log_stderr("--- Banco Vetorial Criado com Sucesso ---")

    def recuperar_documentos(self, query):
        return self.retriever.invoke(query)

    def buscar_contexto(self, query):
        docs = self.recuperar_documentos(query)
        return "\n\n".join([doc.page_content for doc in docs])
