#!/usr/bin/env python3
# monitor_completo.py - Executa todos os monitoramentos

import subprocess
import json
import os
from datetime import datetime

class MonitorCompleto:
    def __init__(self):
        self.base_dir = os.path.expanduser("~/monitor_asus_rog")
        self.scripts_dir = f"{self.base_dir}/scripts"
    
    def executar_monitoramento_completo(self):
        """Executa todos os scripts de monitoramento"""
        print("🚀 === MONITORAMENTO COMPLETO INICIADO ===")
        print(f"⏰ {datetime.now()}")
        
        resultados = {
            'timestamp': datetime.now().isoformat(),
            'mercadolivre': [],
            'olx': [],
            'facebook': 'manual',
            'total_candidatos': 0,
            'alertas_maximos': 0
        }
        
        # 1. Mercado Livre
        print("\n🛒 Executando monitoramento Mercado Livre...")
        try:
            result = subprocess.run(
                ['python3', f"{self.scripts_dir}/monitor_asus_rog.py"],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                print("✅ Mercado Livre concluído")
                resultados['mercadolivre'] = self.carregar_ultimos_resultados('candidatos_')
            else:
                print(f"❌ Erro Mercado Livre: {result.stderr}")
        except Exception as e:
            print(f"❌ Erro execução ML: {e}")
        
        # 2. OLX
        print("\n🏪 Executando monitoramento OLX...")
        try:
            result = subprocess.run(
                ['python3', f"{self.scripts_dir}/monitor_olx.py"],
                capture_output=True, text=True, timeout=180
            )
            if result.returncode == 0:
                print("✅ OLX concluído")
                resultados['olx'] = self.carregar_ultimos_resultados('olx_candidatos_')
            else:
                print(f"❌ Erro OLX: {result.stderr}")
        except Exception as e:
            print(f"❌ Erro execução OLX: {e}")
        
        # 3. Análise consolidada
        self.gerar_relatorio_consolidado(resultados)
        
        return resultados
    
    def carregar_ultimos_resultados(self, prefixo):
        """Carrega os últimos resultados de um tipo específico"""
        import glob
        
        pattern = f"{self.base_dir}/resultados/{prefixo}*.json"
        arquivos = sorted(glob.glob(pattern), reverse=True)
        
        if arquivos:
            try:
                with open(arquivos[0], 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def gerar_relatorio_consolidado(self, resultados):
        """Gera relatório consolidado de todos os sites"""
        ml_candidatos = resultados.get('mercadolivre', [])
        olx_candidatos = resultados.get('olx', [])
        
        total_candidatos = len(ml_candidatos) + len(olx_candidatos)
        
        # Contar alertas máximos
        alertas_ml = len([c for c in ml_candidatos if c.get('score_total', 0) >= 35])
        alertas_olx = len([c for c in olx_candidatos if c.get('score_total', 0) >= 40])
        total_alertas = alertas_ml + alertas_olx
        
        # Gerar relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        relatorio_file = f"{self.base_dir}/resultados/relatorio_consolidado_{timestamp}.json"
        
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'resumo': {
                'total_candidatos': total_candidatos,
                'mercadolivre_candidatos': len(ml_candidatos),
                'olx_candidatos': len(olx_candidatos),
                'alertas_maximos_total': total_alertas,
                'alertas_mercadolivre': alertas_ml,
                'alertas_olx': alertas_olx
            },
            'top_candidatos': self.obter_top_candidatos(ml_candidatos, olx_candidatos),
            'detalhes': {
                'mercadolivre': ml_candidatos,
                'olx': olx_candidatos
            }
        }
        
        with open(relatorio_file, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        self.imprimir_resumo(relatorio)
        return relatorio_file
    
    def obter_top_candidatos(self, ml_candidatos, olx_candidatos):
        """Obtém os top 10 candidatos de todos os sites"""
        todos_candidatos = []
        
        for candidato in ml_candidatos:
            candidato['origem'] = 'Mercado Livre'
            todos_candidatos.append(candidato)
        
        for candidato in olx_candidatos:
            candidato['origem'] = 'OLX'
            todos_candidatos.append(candidato)
        
        # Ordenar por score total
        todos_candidatos.sort(key=lambda x: x.get('score_total', 0), reverse=True)
        
        return todos_candidatos[:10]
    
    def imprimir_resumo(self, relatorio):
        """Imprime resumo do monitoramento"""
        resumo = relatorio['resumo']
        
        print("\n" + "="*60)
        print("📊 RESUMO DO MONITORAMENTO COMPLETO")
        print("="*60)
        print(f"🎯 Total de candidatos encontrados: {resumo['total_candidatos']}")
        print(f"   🛒 Mercado Livre: {resumo['mercadolivre_candidatos']}")
        print(f"   🏪 OLX: {resumo['olx_candidatos']}")
        print(f"\n🚨 Alertas máximos: {resumo['alertas_maximos_total']}")
        print(f"   🛒 ML: {resumo['alertas_mercadolivre']}")
        print(f"   🏪 OLX: {resumo['alertas_olx']}")
        
        if resumo['alertas_maximos_total'] > 0:
            print(f"\n⚠️ AÇÃO NECESSÁRIA: {resumo['alertas_maximos_total']} candidatos de alta prioridade!")
            print("📋 Verifique o relatório detalhado e considere investigação.")
        
        # Top 5 candidatos
        top_candidatos = relatorio['top_candidatos'][:5]
        if top_candidatos:
            print(f"\n🏆 TOP 5 CANDIDATOS:")
            for i, candidato in enumerate(top_candidatos, 1):
                print(f"{i}. {candidato.get('nivel_alerta', 'N/A')} - Score: {candidato.get('score_total', 0)}")
                print(f"   📝 {candidato.get('titulo', 'N/A')[:50]}...")
                print(f"   💰 R$ {candidato.get('preco', 0):,} - {candidato.get('origem', 'N/A')}")

# Execução principal
if __name__ == "__main__":
    monitor = MonitorCompleto()
    resultados = monitor.executar_monitoramento_completo()