#!/bin/bash
# monitor_continuo.sh - Execução contínua

BASE_DIR="$HOME/monitor_asus_rog"
LOG_FILE="$BASE_DIR/logs/monitor.log"
ALERTAS_DIR="$BASE_DIR/alertas"

# Criar logs se não existir
mkdir -p "$BASE_DIR/logs"
mkdir -p "$ALERTAS_DIR"

echo "🔄 === MONITORAMENTO CONTÍNUO INICIADO $(date) ===" | tee -a "$LOG_FILE"

while true; do
    echo -e "\n⏰ --- CICLO $(date) ---" | tee -a "$LOG_FILE"
    
    # Executar monitoramento
    cd "$BASE_DIR/scripts"
    python3 monitor_asus_rog.py | tee -a "$LOG_FILE"
    
    # Verificar alertas recentes
    ARQUIVO_RECENTE=$(ls -t "$BASE_DIR/resultados/"*.json 2>/dev/null | head -1)
    
    if [ -f "$ARQUIVO_RECENTE" ]; then
        CANDIDATOS_ALTO_SCORE=$(python3 -c "
import json, sys
try:
    with open('$ARQUIVO_RECENTE', 'r') as f:
        dados = json.load(f)
    alto_score = [c for c in dados if c.get('score_total', 0) >= 35]
    print(len(alto_score))
except:
    print(0)
")
        
        if [ "$CANDIDATOS_ALTO_SCORE" -gt 0 ]; then
            echo "🚨 $CANDIDATOS_ALTO_SCORE CANDIDATOS DE ALTO SCORE!" | tee -a "$LOG_FILE"
            echo "$(date): $CANDIDATOS_ALTO_SCORE candidatos alto score encontrados" > "$ALERTAS_DIR/alerta_$(date +%Y%m%d_%H%M%S).txt"
            echo "Arquivo: $ARQUIVO_RECENTE" >> "$ALERTAS_DIR/alerta_$(date +%Y%m%d_%H%M%S).txt"
        fi
    fi
    
    echo "⏳ Aguardando 2 horas para próximo ciclo..." | tee -a "$LOG_FILE"
    sleep 7200  # 2 horas
done