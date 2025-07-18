#!/bin/bash
# setup.sh - Configuração inicial

echo "🔧 Configurando Monitor ASUS ROG Zephyrus M16..."

# Instalar dependências Python
echo "🐍 Instalando dependências Python..."
pip3 install requests beautifulsoup4 lxml --user

# Dar permissões aos scripts
echo "🔐 Configurando permissões..."
find ~/monitor_asus_rog/scripts -name "*.sh" -exec chmod +x {} \;
find ~/monitor_asus_rog/scripts -name "*.py" -exec chmod +x {} \;

# Criar arquivo de configuração
echo "⚙️ Criando configurações..."
cat > ~/monitor_asus_rog/config/config.json << 'CONFIG_EOF'
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

echo "✅ Configuração concluída!"
echo "📂 Projeto em: ~/monitor_asus_rog/"
echo "🚀 Para teste: cd scripts && python3 monitor_asus_rog.py"