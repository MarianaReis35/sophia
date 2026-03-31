# 🚀 Guia Rápido - SOPHIA

## ✅ Todas as Correções Aplicadas!

### O que foi corrigido:
1. ✅ **Dependências instaladas** - FastHTML, FastAPI, pandas, google-genai
2. ✅ **API atualizada** - Migrado para `google.genai` (sem warnings!)
3. ✅ **Caixa de conversa** - Mensagens de boas-vindas adicionadas
4. ✅ **Imagem de fundo** - CSS corrigido com imagem do Unsplash
5. ✅ **Ambos arquivos atualizados** - sophia.py e sophia_nova.py

---

## 🎯 Como Rodar (3 passos):

### 1️⃣ Entre no ambiente virtual:
```bash
cd "/Users/marianareis/Documents/Doutorado em Políticas Públicas/S.O.P.H.I.A/sophia"
source venv/bin/activate
```

### 2️⃣ (Opcional) Instale/atualize dependências:
```bash
pip install -r requirements.txt
```

### 3️⃣ Rode o servidor:
```bash
python sophia.py
```

**Ou use o script:**
```bash
./run.sh
```

---

## 🌐 Acesso

Após iniciar, acesse no navegador:
- **URL:** http://localhost:5001

---

## 📋 Checklist Pré-Execução

- [ ] Arquivo `.env` existe com `CHAVE_DE_API=sua_chave`
- [ ] Arquivo `Personalidade.md` existe
- [ ] Pasta `DataLake/` existe (pode estar vazia)
- [ ] Ambiente virtual `venv/` está ativado

---

## 🆘 Solução de Problemas

### Erro: "No module named 'fasthtml'"
```bash
pip install python-fasthtml
```

### Erro: "No module named 'google.genai'"
```bash
pip install google-genai
```

### Erro: "CHAVE_DE_API not found"
Crie/edite o arquivo `.env`:
```
CHAVE_DE_API=sua_chave_do_gemini_aqui
```

### Porta já em uso
O FastHTML escolherá automaticamente outra porta disponível.

---

## 📚 Arquivos Importantes

- `sophia.py` - Versão completa com upload de arquivos
- `sophia_nova.py` - Versão simplificada com seletor de modelo
- `CORRECOES.md` - Documentação detalhada das correções
- `requirements.txt` - Todas as dependências

---

## 🎨 Recursos da Interface

- 💬 Chat interativo com HTMX
- 📁 Upload de múltiplos formatos (CSV, PDF, imagens, etc.)
- 🎨 Fundo temático do Sul Global
- 📖 Glossário estatístico interativo
- 🤖 Integração com Gemini 2.0 Flash

---

**Tudo pronto para usar! 🎉**
