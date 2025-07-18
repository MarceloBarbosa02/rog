#!/bin/bash
# setup.sh - Configuração inicial

echo "🔧 Configurando Monitor ASUS ROG Zephyrus M16..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale com: brew install python"
    exit 1
fi

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado!"
else
    echo "📦 Ambiente virtual já existe!"
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install -r requirements.txt

# Dar permissões aos scripts
echo "🔐 Configurando permissões..."
find ./scripts -name "*.sh" -exec chmod +x {} \;
find ./scripts -name "*.py" -exec chmod +x {} \;

# Criar arquivo de configuração
echo "⚙️ Criando configurações..."
cat > ./config/config.json << 'CONFIG_EOF'
{
    "modelo": "ASUS ROG Zephyrus M16",
    "codigo": "GU604",
    "ano": "2023",
    "preco_suspeito_max": 8000,
    "preco_muito_suspeito": 5000,
    "intervalo_horas": 2,
    "email_alertas": "",
    "sites_monitorar": ["mercadolivre", "olx"],
    "caracteristicas_unicas": [
        "anime matrix",
        "mini led", 
        "240hz",
        "2560x1600",
        "gu604",
        "nebula hdr"
    ]
}
CONFIG_EOF

echo ""
echo "✅ Configuração concluída!"
echo "📂 Projeto configurado em ambiente virtual"
echo ""
echo "🚀 Para usar o projeto:"
echo "   1. Ative o ambiente virtual: source venv/bin/activate"
echo "   2. Execute os scripts: cd scripts && python3 monitor_asus_rog.py"
echo ""
echo "💡 Lembre-se de ativar o ambiente virtual sempre que usar o projeto!"