# SOPHIA - Sistema Operacional de Pesquisa Humana e Intelectual Avançada

## 📋 Descrição

SOPHIA é uma Assistente Virtual de Pesquisa e Analista de Dados Sênior especializada em políticas públicas. O sistema utiliza Inteligência Artificial (Google Gemini) combinada com RAG (Retrieval-Augmented Generation) para análise de dados e documentos relacionados a políticas públicas na América Latina.

### Principais Funcionalidades

- 🤖 Assistente conversacional especializada em análise de políticas públicas
- 📊 Análise de dados em formato CSV com estatísticas descritivas
- 📄 Processamento de documentos (PDF, Word, Excel, PowerPoint, texto)
- 🖼️ Suporte para análise de imagens
- 🔍 Sistema RAG para consulta em base de conhecimento (Data Lake)
- 📚 Glossário interativo de termos estatísticos
- 🎨 Interface web moderna e responsiva

---

## 🚀 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para clonar o repositório)

### Verificar instalação do Python

```bash
python --version
# ou
python3 --version
```

---

## 📦 Instalação

### Opção 1: Instalação Local (Recomendado para Avaliação)

#### 1. Clone ou baixe o projeto

```bash
# Se tiver Git instalado:
git clone <url-do-repositorio>
cd sophia

# Ou extraia o arquivo ZIP do projeto e navegue até a pasta
```

#### 2. Crie um ambiente virtual (recomendado)

```bash
# No Windows:
python -m venv venv
venv\Scripts\activate

# No macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Configure a chave da API

O arquivo `.env` já está incluído no projeto com a chave de API configurada. Caso precise alterá-la:

```bash
# Edite o arquivo .env e adicione sua chave do Google Gemini:
CHAVE_DE_API=sua_chave_aqui
```

Para obter uma chave gratuita do Google Gemini: https://aistudio.google.com/app/apikey

#### 5. Execute o projeto

```bash
python sophia.py
```

#### 6. Acesse a aplicação

Abra seu navegador e acesse:
```
http://localhost:7860
```

---

### Opção 2: Instalação com Docker

#### 1. Certifique-se de ter o Docker instalado

- **Docker Desktop**: [Download](https://www.docker.com/products/docker-desktop/)

#### 2. Execute com Docker Compose

```bash
# Na pasta do projeto:
docker-compose up --build
```

#### 3. Acesse a aplicação

```
http://localhost:7860
```

Para parar a aplicação:
```bash
docker-compose down
```

---

## 📖 Como Usar

### 1. Interface Principal

Ao acessar a aplicação, você verá:
- **Janela de chat**: Área de conversação com a SOPHIA
- **Campo de mensagem**: Digite suas perguntas e análises
- **Botão de anexar**: Faça upload de arquivos para análise
- **Contador do Data Lake**: Mostra quantos documentos estão disponíveis

### 2. Fazendo Perguntas

Digite perguntas relacionadas a políticas públicas, estatística ou análise de dados:

```
Exemplos:
- "Explique o que é p-valor"
- "Como interpretar significância estatística?"
- "Quais são os principais indicadores de políticas sociais?"
```

### 3. Upload de Arquivos

Clique em "📎 Anexar arquivo" e selecione:
- **CSV**: Para análise estatística de dados
- **PDF/Word/Excel**: Para extração e análise de conteúdo
- **Imagens**: Para análise visual
- **Código**: Python, JavaScript, HTML, CSS, JSON, etc.

Após o upload, faça perguntas sobre o arquivo:
```
- "Faça uma análise descritiva desses dados"
- "Quais são as principais tendências?"
- "Resuma este documento"
```

### 4. Consultando o Data Lake

A SOPHIA tem acesso aos documentos na pasta `DataLake/`. Para consultar:

```
- "O que os documentos dizem sobre previdência social no Chile?"
- "Busque informações sobre seguridade social"
```

### 5. Glossário Interativo

Termos estatísticos aparecem destacados em **lilás e negrito**. Clique neles para ver a definição.

---

## 📁 Estrutura do Projeto

```
sophia/
├── sophia.py              # Aplicação principal
├── motor_rag.py          # Motor de busca RAG
├── Personalidade.md      # Instruções de comportamento da IA
├── requirements.txt      # Dependências Python
├── .env                  # Configurações (chave API)
├── Dockerfile           # Configuração Docker
├── docker-compose.yml   # Orquestração Docker
├── DataLake/           # Documentos para consulta RAG
│   ├── L8213consol.pdf
│   └── Libro-100-anos-Seguridad-Social no Chile.pdf
└── README.md           # Este arquivo
```

---

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError"

```bash
# Certifique-se de que o ambiente virtual está ativado e reinstale:
pip install -r requirements.txt
```

### Erro: "API Key inválida"

Verifique se o arquivo `.env` contém uma chave válida do Google Gemini.

### Porta 7860 já em uso

```bash
# Edite sophia.py e altere a porta:
# Procure por: serve(port=7860)
# Altere para: serve(port=8080)
```

### Problemas com FAISS no Windows

```bash
# Se houver erro com faiss-cpu, tente:
pip uninstall faiss-cpu
pip install faiss-cpu --no-cache-dir
```

---

## 🛠️ Tecnologias Utilizadas

- **FastHTML**: Framework web Python
- **Google Gemini**: Modelo de linguagem (IA)
- **LangChain**: Framework para aplicações com LLM
- **FAISS**: Busca vetorial para RAG
- **Sentence Transformers**: Embeddings de texto
- **Pandas**: Análise de dados
- **PyPDF**: Processamento de PDFs

---

## 📚 Contexto Acadêmico

Este projeto foi desenvolvido como ferramenta de apoio à pesquisa em políticas públicas, com foco em:

- Análise comparativa de sistemas de seguridade social na América Latina
- Perspectiva crítica baseada nas Epistemologias do Sul
- Rigor estatístico e metodológico em pesquisas sociais
- Democratização do acesso a análises de dados complexas

---

## 👥 Autoria

Desenvolvido como parte do Doutorado em Políticas Públicas.

---

## 📝 Licença

Este projeto é de uso acadêmico e educacional.

---

## 📞 Suporte

Para dúvidas sobre o funcionamento do sistema:

1. Verifique a seção de **Solução de Problemas**
2. Consulte os logs no terminal onde a aplicação está rodando
3. Verifique se todas as dependências foram instaladas corretamente

---

## 🎯 Checklist para Avaliação

- [ ] Python 3.11+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Arquivo `.env` configurado
- [ ] Aplicação rodando (`python sophia.py`)
- [ ] Navegador acessando `http://localhost:7860`
- [ ] Teste de conversação funcionando
- [ ] Upload de arquivo CSV funcionando
- [ ] Consulta ao Data Lake funcionando

---

**Versão**: 1.0  
**Última atualização**: 2024
