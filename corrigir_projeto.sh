#!/bin/bash
# corrigir_projeto.sh - Correção automática de problemas

echo "🔧 === CORREÇÃO AUTOMÁTICA DO PROJETO ==="
echo ""

# 1. Criar estrutura de pastas
echo "📁 Criando estrutura de pastas..."
mkdir -p scripts
mkdir -p resultados
mkdir -p logs
mkdir -p alertas
mkdir -p config
echo "✅ Pastas criadas!"

# 2. Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "⚠️ Não parece estar no diretório do projeto"
    echo "💡 Certifique-se de estar em: cd ~/monitor_asus_rog"
fi

# 3. Configurar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "🐍 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado!"
fi

# 4. Ativar ambiente virtual e instalar dependências
echo "📦 Configurando dependências..."
source venv/bin/activate
pip install requests beautifulsoup4 lxml --quiet
echo "✅ Dependências instaladas!"

# 5. Criar config básico se não existir
if [ ! -f "config/config.json" ]; then
    echo "⚙️ Criando configuração básica..."
    cat > config/config.json << 'EOF'
{
    "modelo": "ASUS ROG Zephyrus M16",
    "codigo": "GU604",
    "ano": "2023",
    "preco_suspeito_max": 8000,
    "preco_muito_suspeito": 5000,
    "intervalo_horas": 2,
    "email_alertas": "",
    "sites_monitorar": [
        "mercadolivre",
        "olx", 
        "shopee",
        "enjoei"
    ]
}
EOF
    echo "✅ Configuração criada!"
fi

# 6. Dar permissões
echo "🔐 Configurando permissões..."
chmod +x *.sh 2>/dev/null
chmod +x scripts/*.py 2>/dev/null
chmod +x scripts/*.sh 2>/dev/null
echo "✅ Permissões configuradas!"

echo ""
echo "🎉 === CORREÇÃO CONCLUÍDA ==="
echo ""
echo "🚀 Para testar se funciona:"
echo "   python3 monitor_simples.py"
echo ""
echo "🎯 Para monitoramento completo:"
echo "   source venv/bin/activate"
echo "   python3 scripts/monitor_completo.py"
echo ""
echo "📋 Scripts principais disponíveis:"
echo "   - monitor_simples.py (teste básico)"
echo "   - scripts/monitor_enjoei.py (prioritário para usados)"
echo "   - scripts/monitor_olx.py (classificados)"
echo "   - scripts/monitor_completo.py (todos os sites)" 