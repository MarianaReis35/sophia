#!/bin/bash

echo "🔍 Testando SOPHIA - Validação das Correções"
echo "=============================================="
echo ""

cd "/Users/marianareis/Documents/Doutorado em Políticas Públicas/S.O.P.H.I.A/sophia"
source venv/bin/activate

echo "1️⃣ Testando imports..."
python -c "
from google import genai
from fasthtml.common import *
import pandas as pd
print('   ✅ Todos os imports funcionando!')
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ Imports OK"
else
    echo "   ❌ Erro nos imports"
    exit 1
fi

echo ""
echo "2️⃣ Testando carregamento do sophia.py..."
python -c "
import sys
sys.path.insert(0, '.')
from sophia import app, rt, custom_css
print('   ✅ sophia.py carregado!')
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ sophia.py OK"
else
    echo "   ❌ Erro ao carregar sophia.py"
    exit 1
fi

echo ""
echo "3️⃣ Verificando arquivos necessários..."

if [ -f ".env" ]; then
    echo "   ✅ .env encontrado"
else
    echo "   ⚠️  .env não encontrado (necessário para API)"
fi

if [ -f "Personalidade.md" ]; then
    echo "   ✅ Personalidade.md encontrado"
else
    echo "   ⚠️  Personalidade.md não encontrado"
fi

if [ -d "DataLake" ]; then
    echo "   ✅ DataLake/ encontrado"
    pdf_count=$(ls -1 DataLake/*.pdf 2>/dev/null | wc -l)
    echo "   📚 $pdf_count PDFs no DataLake"
else
    echo "   ⚠️  DataLake/ não encontrado"
fi

echo ""
echo "4️⃣ Verificando dependências..."
pip list | grep -E "fasthtml|fastapi|pandas|google-genai" | while read line; do
    echo "   ✅ $line"
done

echo ""
echo "=============================================="
echo "✨ Validação Completa!"
echo ""
echo "Para rodar o servidor:"
echo "  python sophia.py"
echo ""
echo "Ou use:"
echo "  ./run.sh"
echo "=============================================="
