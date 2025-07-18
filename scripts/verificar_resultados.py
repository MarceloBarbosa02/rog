#!/usr/bin/env python3
# verificar_resultados.py - Análise dos resultados

import json
import glob
import os
from datetime import datetime

def analisar_resultados():
    base_dir = os.path.expanduser("~/monitor_asus_rog")
    arquivos = glob.glob(f"{base_dir}/resultados/*.json")
    
    if not arquivos:
        print("📭 Nenhum resultado encontrado ainda.")
        return
    
    print(f"📊 Analisando {len(arquivos)} arquivo(s) de resultados...")
    
    todos_candidatos = []
    for arquivo in sorted(arquivos):
        try:
            with open(arquivo, 'r') as f:
                dados = json.load(f)
                if isinstance(dados, list):
                    todos_candidatos.extend(dados)
                else:
                    todos_candidatos.append(dados)
        except:
            continue
    
    if not todos_candidatos:
        print("📭 Nenhum candidato encontrado nos arquivos.")
        return
    
    # Estatísticas
    print(f"\n📈 ESTATÍSTICAS:")
    print(f"   Total de candidatos: {len(todos_candidatos)}")
    
    alertas_maximos = [c for c in todos_candidatos if c.get('score_total', 0) >= 35]
    alertas_altos = [c for c in todos_candidatos if 30 <= c.get('score_total', 0) < 35]
    alertas_medios = [c for c in todos_candidatos if 20 <= c.get('score_total', 0) < 30]
    
    print(f"   🚨 Alertas Máximos: {len(alertas_maximos)}")
    print(f"   ⚠️ Alertas Altos: {len(alertas_altos)}")
    print(f"   ⚠️ Alertas Médios: {len(alertas_medios)}")
    
    # Mostrar top 5 candidatos
    candidatos_ordenados = sorted(todos_candidatos, 
                                 key=lambda x: x.get('score_total', 0), 
                                 reverse=True)
    
    print(f"\n🏆 TOP 5 CANDIDATOS:")
    for i, candidato in enumerate(candidatos_ordenados[:5], 1):
        print(f"\n{i}. {candidato.get('nivel_alerta', 'N/A')} (Score: {candidato.get('score_total', 0)})")
        print(f"   {candidato.get('titulo', 'N/A')}")
        print(f"   R$ {candidato.get('preco', 0):,} - {candidato.get('site', 'N/A')}")

if __name__ == "__main__":
    analisar_resultados()