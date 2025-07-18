#!/bin/bash
# activate.sh - Ativa o ambiente virtual

if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "🔧 Execute primeiro: ./setup.sh"
    exit 1
fi

echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate
echo "✅ Ambiente virtual ativado!"
echo "📂 Você está no projeto Monitor ASUS ROG"
echo ""
echo "💡 Scripts disponíveis em ./scripts/"
echo "   - monitor_asus_rog.py (monitoramento principal)"
echo "   - monitor_completo.py (monitoramento completo)"
echo "   - analise_avancada.py (análise avançada)"
echo "   - verificar_resultados.py (verificar resultados)"
echo ""
echo "🚀 Para executar: python3 scripts/monitor_asus_rog.py" 