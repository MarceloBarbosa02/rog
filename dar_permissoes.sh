#!/bin/bash
# dar_permissoes.sh - Script para dar permissões de execução

echo "🔐 Configurando permissões para todos os scripts..."

# Scripts principais
chmod +x setup.sh
chmod +x activate.sh

# Scripts Python de monitoramento
chmod +x scripts/monitor_asus_rog.py
chmod +x scripts/monitor_olx.py
chmod +x scripts/monitor_facebook.py
chmod +x scripts/monitor_completo.py
chmod +x scripts/monitor_continuo.sh
chmod +x scripts/analise_avancada.py
chmod +x scripts/verificar_resultados.py

# Novos scripts implementados
chmod +x scripts/monitor_shopee.py
chmod +x scripts/monitor_magalu.py
chmod +x scripts/monitor_enjoei.py
chmod +x scripts/monitor_americanas.py
chmod +x scripts/monitor_casasbahia.py
chmod +x scripts/monitor_pontofrio.py
chmod +x scripts/monitor_ebay.py

echo "✅ Permissões configuradas para todos os scripts!"
echo ""
echo "📋 Scripts disponíveis:"
echo "   🔧 setup.sh - Configuração inicial"
echo "   🔄 activate.sh - Ativar ambiente virtual"
echo ""
echo "   📊 Monitor individual por site:"
echo "   🛒 scripts/monitor_asus_rog.py (Mercado Livre)"
echo "   🏪 scripts/monitor_olx.py (OLX)"
echo "   🛍️ scripts/monitor_shopee.py (Shopee)"
echo "   🏬 scripts/monitor_magalu.py (Magazine Luiza)"
echo "   ♻️ scripts/monitor_enjoei.py (Enjoei - PRIORITÁRIO)"
echo "   🇺🇸 scripts/monitor_americanas.py (Americanas)"
echo "   🏠 scripts/monitor_casasbahia.py (Casas Bahia)"
echo "   ❄️ scripts/monitor_pontofrio.py (Ponto Frio)"
echo "   🌎 scripts/monitor_ebay.py (eBay Brasil)"
echo "   📱 scripts/monitor_facebook.py (Facebook - Manual)"
echo ""
echo "   📈 Análise e relatórios:"
echo "   🔍 scripts/monitor_completo.py (TODOS os sites)"
echo "   🔄 scripts/monitor_continuo.sh (Monitoramento contínuo)"
echo "   📊 scripts/analise_avancada.py (Análise de tendências)"
echo "   ✅ scripts/verificar_resultados.py (Verificar resultados)"
echo ""
echo "🚀 Para usar: ./setup.sh && source activate.sh" 