#!/bin/bash
# diagnostico.sh - Verifica e corrige problemas do projeto

echo "🔍 === DIAGNÓSTICO DO PROJETO MONITOR ASUS ROG ==="
echo ""

# 1. Verificar onde estamos
echo "📂 Diretório atual:"
pwd
echo ""

# 2. Verificar se existe a pasta scripts
echo "📁 Verificando estrutura de pastas:"
ls -la
echo ""

# 3. Verificar scripts na pasta scripts
echo "🐍 Scripts disponíveis:"
if [ -d "scripts" ]; then
    ls -la scripts/
else
    echo "❌ Pasta scripts não encontrada!"
    echo "🔧 Criando pasta scripts..."
    mkdir -p scripts
fi
echo ""

# 4. Criar pastas necessárias
echo "📁 Criando pastas necessárias..."
mkdir -p resultados
mkdir -p logs
mkdir -p alertas
mkdir -p config
echo "✅ Pastas criadas!"
echo ""

# 5. Verificar se scripts existem
echo "🔍 Verificando scripts principais:"
scripts_necessarios=(
    "monitor_asus_rog.py"
    "monitor_olx.py"
    "monitor_enjoei.py"
    "monitor_completo.py"
    "monitor_shopee.py"
)

for script in "${scripts_necessarios[@]}"; do
    if [ -f "scripts/$script" ]; then
        echo "✅ $script - OK"
    else
        echo "❌ $script - FALTANDO"
    fi
done
echo ""

# 6. Dar permissões
echo "🔐 Configurando permissões..."
chmod +x scripts/*.py 2>/dev/null
chmod +x scripts/*.sh 2>/dev/null
chmod +x *.sh 2>/dev/null
echo "✅ Permissões configuradas!"
echo ""

# 7. Verificar Python e dependências
echo "🐍 Verificando Python:"
python3 --version
echo ""

# 8. Verificar se ambiente virtual existe
echo "📦 Verificando ambiente virtual:"
if [ -d "venv" ]; then
    echo "✅ Ambiente virtual encontrado"
else
    echo "❌ Ambiente virtual não encontrado"
    echo "🔧 Execute: python3 -m venv venv"
fi
echo ""

echo "🎯 === COMANDOS PARA CORRIGIR ==="
echo ""
echo "1. Se os scripts estão faltando:"
echo "   git pull  # Para baixar os arquivos mais recentes"
echo ""
echo "2. Se ambiente virtual não existe:"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install requests beautifulsoup4 lxml"
echo ""
echo "3. Para executar monitoramento:"
echo "   source venv/bin/activate"
echo "   python3 scripts/monitor_enjoei.py    # Prioritário para usados"
echo "   python3 scripts/monitor_completo.py  # Todos os sites"
echo ""
echo "🎉 Diagnóstico concluído!" 