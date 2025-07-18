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
            'shopee': [],
            'magalu': [],
            'enjoei': [],
            'americanas': [],
            'casasbahia': [],
            'pontofrio': [],
            'ebay': [],
            'facebook': 'manual',
            'total_candidatos': 0,
            'alertas_maximos': 0
        }
        
        sites_monitoramento = [
            ('Mercado Livre', 'monitor_asus_rog.py', 'candidatos_', '🛒'),
            ('OLX', 'monitor_olx.py', 'olx_candidatos_', '🏪'),
            ('Shopee', 'monitor_shopee.py', 'shopee_candidatos_', '🛍️'),
            ('Magazine Luiza', 'monitor_magalu.py', 'magalu_candidatos_', '🏬'),
            ('Enjoei', 'monitor_enjoei.py', 'enjoei_candidatos_', '♻️'),
            ('Americanas', 'monitor_americanas.py', 'americanas_candidatos_', '🇺🇸'),
            ('Casas Bahia', 'monitor_casasbahia.py', 'casasbahia_candidatos_', '🏠'),
            ('Ponto Frio', 'monitor_pontofrio.py', 'pontofrio_candidatos_', '❄️'),
            ('eBay', 'monitor_ebay.py', 'ebay_candidatos_', '🌎')
        ]
        
        for nome_site, script, prefixo_arquivo, emoji in sites_monitoramento:
            print(f"\n{emoji} Executando monitoramento {nome_site}...")
            try:
                result = subprocess.run(
                    ['python3', f"{self.scripts_dir}/{script}"],
                    capture_output=True, text=True, timeout=180
                )
                if result.returncode == 0:
                    print(f"✅ {nome_site} concluído")
                    chave = nome_site.lower().replace(' ', '').replace('é', 'e')
                    if chave == 'mercadolivre':
                        chave = 'mercadolivre'
                    elif chave == 'magazineluiza':
                        chave = 'magalu'
                    resultados[chave] = self.carregar_ultimos_resultados(prefixo_arquivo)
                else:
                    print(f"❌ Erro {nome_site}: {result.stderr}")
            except Exception as e:
                print(f"❌ Erro execução {nome_site}: {e}")
        
        # Análise consolidada
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
        # Coletar candidatos de todos os sites
        todos_candidatos = []
        total_alertas = 0
        
        sites_dados = {
            'mercadolivre': ('Mercado Livre', 35),
            'olx': ('OLX', 40),
            'shopee': ('Shopee', 35),
            'magalu': ('Magazine Luiza', 35),
            'enjoei': ('Enjoei', 30),  # Threshold menor para usados
            'americanas': ('Americanas', 35),
            'casasbahia': ('Casas Bahia', 35),
            'pontofrio': ('Ponto Frio', 35),
            'ebay': ('eBay', 35)
        }
        
        for site_key, (nome_site, threshold) in sites_dados.items():
            candidatos = resultados.get(site_key, [])
            todos_candidatos.extend(candidatos)
            alertas_site = len([c for c in candidatos if c.get('score_total', 0) >= threshold])
            total_alertas += alertas_site
        
        total_candidatos = len(todos_candidatos)
        
        # Gerar relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        relatorio_file = f"{self.base_dir}/resultados/relatorio_consolidado_{timestamp}.json"
        
        # Criar resumo por site
        resumo_sites = {}
        alertas_por_site = {}
        for site_key, (nome_site, threshold) in sites_dados.items():
            candidatos = resultados.get(site_key, [])
            resumo_sites[f"{site_key}_candidatos"] = len(candidatos)
            alertas_por_site[f"alertas_{site_key}"] = len([c for c in candidatos if c.get('score_total', 0) >= threshold])
        
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'resumo': {
                'total_candidatos': total_candidatos,
                **resumo_sites,
                'alertas_maximos_total': total_alertas,
                **alertas_por_site
            },
            'top_candidatos': self.obter_top_candidatos_todos(todos_candidatos),
            'detalhes': resultados
        }
        
        with open(relatorio_file, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        self.imprimir_resumo(relatorio)
        return relatorio_file
    
    def obter_top_candidatos_todos(self, todos_candidatos):
        """Obtém os top 10 candidatos de todos os sites"""
        # Adicionar origem se não existir
        for candidato in todos_candidatos:
            if 'origem' not in candidato:
                candidato['origem'] = candidato.get('site', 'Desconhecido')
        
        # Ordenar por score total
        todos_candidatos.sort(key=lambda x: x.get('score_total', 0), reverse=True)
        
        return todos_candidatos[:10]
    
    def obter_top_candidatos(self, ml_candidatos, olx_candidatos):
        """Obtém os top 10 candidatos de todos os sites (método legado)"""
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
        
        # Mostrar candidatos por site
        sites_emojis = {
            'mercadolivre': '🛒',
            'olx': '🏪',
            'shopee': '🛍️',
            'magalu': '🏬',
            'enjoei': '♻️',
            'americanas': '🇺🇸',
            'casasbahia': '🏠',
            'pontofrio': '❄️',
            'ebay': '🌎'
        }
        
        for site, emoji in sites_emojis.items():
            candidatos_key = f"{site}_candidatos"
            if candidatos_key in resumo:
                nome_site = site.replace('magalu', 'Magazine Luiza').replace('casasbahia', 'Casas Bahia').replace('pontofrio', 'Ponto Frio').title()
                print(f"   {emoji} {nome_site}: {resumo[candidatos_key]}")
        
        print(f"\n🚨 Alertas máximos: {resumo['alertas_maximos_total']}")
        
        # Mostrar alertas por site
        for site, emoji in sites_emojis.items():
            alertas_key = f"alertas_{site}"
            if alertas_key in resumo and resumo[alertas_key] > 0:
                nome_site = site.replace('magalu', 'Magazine Luiza').replace('casasbahia', 'Casas Bahia').replace('pontofrio', 'Ponto Frio').title()
                print(f"   {emoji} {nome_site}: {resumo[alertas_key]}")
        
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