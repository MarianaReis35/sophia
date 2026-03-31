#!/bin/bash

# Script para rodar a SOPHIA

echo "🚀 Iniciando SOPHIA..."

# Ativa o ambiente virtual
source venv/bin/activate

# Instala/atualiza dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Roda o servidor
echo "✨ Iniciando servidor FastHTML..."
python sophia.py
