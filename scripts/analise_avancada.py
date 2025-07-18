#!/usr/bin/env python3
# analise_avancada.py - Análise avançada e relatórios

import json
import glob
import os
from datetime import datetime, timedelta
import statistics

class AnaliseAvancada:
    def __init__(self):
        self.base_dir = os.path.expanduser("~/monitor_asus_rog")
        self.resultados_dir = f"{self.base_dir}/resultados"
    
    def analisar_tendencias(self, dias=7):
        """Analisa tendências dos últimos X dias"""
        print(f"📈 Analisando tendências dos últimos {dias} dias...")
        
        # Carregar todos os arquivos dos últimos dias
        arquivos = self.obter_arquivos_periodo(dias)
        
        dados_por_dia = {}
        todos_candidatos = []
        
        for arquivo in arquivos:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    
                # Extrair data do nome do arquivo
                nome_arquivo = os.path.basename(arquivo)
                data_str = nome_arquivo.split('_')[1]  # Formato: YYYYMMDD
                data = datetime.strptime(data_str, "%Y%m%d").date()
                
                if data not in dados_por_dia:
                    dados_por_dia[data] = []
                
                if isinstance(dados, list):
                    dados_por_dia[data].extend(dados)
                    todos_candidatos.extend(dados)
                else:
                    dados_por_dia[data].append(dados)
                    todos_candidatos.append(dados)
                    
            except Exception as e:
                continue
        
        # Análises
        self.gerar_relatorio_tendencias(dados_por_dia, todos_candidatos)
    
    def obter_arquivos_periodo(self, dias):
        """Obtém arquivos dos últimos X dias"""
        data_limite = datetime.now() - timedelta(days=dias)
        
        todos_arquivos = glob.glob(f"{self.resultados_dir}/*.json")
        arquivos_periodo = []
        
        for arquivo in todos_arquivos:
            try:
                # Extrair data do nome do arquivo
                nome = os.path.basename(arquivo)
                if '_' in nome and nome.replace('.json', '').split('_')[1].isdigit():
                    data_str = nome.split('_')[1]
                    if len(data_str) == 8:  # YYYYMMDD
                        data_arquivo = datetime.strptime(data_str, "%Y%m%d")
                        if data_arquivo >= data_limite:
                            arquivos_periodo.append(arquivo)
            except:
                continue
        
        return sorted(arquivos_periodo)
    
    def gerar_relatorio_tendencias(self, dados_por_dia, todos_candidatos):
        """Gera relatório de tendências"""
        print("\n📊 RELATÓRIO DE TENDÊNCIAS")
        print("="*50)
        
        # Estatísticas gerais
        if not todos_candidatos:
            print("📭 Nenhum dado disponível para análise.")
            return
        
        total_candidatos = len(todos_candidatos)
        scores = [c.get('score_total', 0) for c in todos_candidatos]
        precos = [c.get('preco', 0) for c in todos_candidatos if c.get('preco', 0) > 0]
        
        print(f"📈 Total de candidatos analisados: {total_candidatos}")
        
        if scores:
            print(f"📊 Score médio: {statistics.mean(scores):.1f}")
            print(f"📊 Score máximo: {max(scores)}")
            print(f"📊 Score mediano: {statistics.median(scores):.1f}")
        
        if precos:
            print(f"💰 Preço médio: R$ {statistics.mean(precos):,.0f}")
            print(f"💰 Preço mínimo: R$ {min(precos):,}")
            print(f"💰 Preço máximo: R$ {max(precos):,}")
        
        # Análise por site
        sites = {}
        for candidato in todos_candidatos:
            site = candidato.get('site', 'Desconhecido')
            if site not in sites:
                sites[site] = []
            sites[site].append(candidato)
        
        print(f"\n🌐 DISTRIBUIÇÃO POR SITE:")
        for site, candidatos in sites.items():
            alertas_altos = len([c for c in candidatos if c.get('score_total', 0) >= 30])
            print(f"   {site}: {len(candidatos)} candidatos ({alertas_altos} alertas altos)")
        
        # Candidatos mais suspeitos
        candidatos_ordenados = sorted(todos_candidatos, 
                                    key=lambda x: x.get('score_total', 0), 
                                    reverse=True)
        
        print(f"\n🎯 TOP 3 CANDIDATOS MAIS SUSPEITOS:")
        for i, candidato in enumerate(candidatos_ordenados[:3], 1):
            print(f"{i}. Score: {candidato.get('score_total', 0)} - {candidato.get('site', 'N/A')}")
            print(f"   📝 {candidato.get('titulo', 'N/A')[:60]}...")
            print(f"   💰 R$ {candidato.get('preco', 0):,}")
            print(f"   🌐 {candidato.get('url', 'N/A')}")
        
        # Padrões suspeitos
        self.analisar_padroes_suspeitos(todos_candidatos)
        
        # Salvar relatório
        self.salvar_relatorio_analise(dados_por_dia, todos_candidatos)
    
    def analisar_padroes_suspeitos(self, candidatos):
        """Analisa padrões que podem indicar o notebook roubado"""
        print(f"\n🔍 ANÁLISE DE PADRÕES SUSPEITOS:")
        
        # Preços extremamente baixos
        precos_suspeitos = [c for c in candidatos if c.get('preco', 0) < 3000 and c.get('preco', 0) > 0]
        print(f"💸 Preços extremamente baixos (< R$ 3.000): {len(precos_suspeitos)}")
        
        # Características únicas encontradas
        anime_matrix = len([c for c in candidatos if 'anime matrix' in c.get('titulo', '').lower()])
        mini_led = len([c for c in candidatos if 'mini led' in c.get('titulo', '').lower()])
        gu604 = len([c for c in candidatos if 'gu604' in c.get('titulo', '').lower()])
        
        print(f"🎯 Com AniMe Matrix: {anime_matrix}")
        print(f"🎯 Com Mini LED: {mini_led}")
        print(f"🎯 Com código GU604: {gu604}")
        
        if anime_matrix > 0 or gu604 > 0:
            print("⚠️ ATENÇÃO: Características muito específicas encontradas!")
        
        # Vendedores com múltiplos anúncios
        vendedores = {}
        for candidato in candidatos:
            vendedor = candidato.get('vendedor', 'Anônimo')
            if vendedor != 'Anônimo':
                if vendedor not in vendedores:
                    vendedores[vendedor] = []
                vendedores[vendedor].append(candidato)
        
        vendedores_multiplos = {v: anuncios for v, anuncios in vendedores.items() if len(anuncios) > 1}
        if vendedores_multiplos:
            print(f"👤 Vendedores com múltiplos anúncios: {len(vendedores_multiplos)}")
            for vendedor, anuncios in vendedores_multiplos.items():
                print(f"   {vendedor}: {len(anuncios)} anúncios")
    
    def salvar_relatorio_analise(self, dados_por_dia, todos_candidatos):
        """Salva relatório de análise em arquivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_relatorio = f"{self.base_dir}/relatorio_analise_{timestamp}.json"
        
        relatorio = {
            'timestamp_analise': datetime.now().isoformat(),
            'periodo_analisado': {
                'inicio': min(dados_por_dia.keys()).isoformat() if dados_por_dia else None,
                'fim': max(dados_por_dia.keys()).isoformat() if dados_por_dia else None
            },
            'estatisticas': {
                'total_candidatos': len(todos_candidatos),
                'candidatos_por_dia': {str(data): len(candidatos) for data, candidatos in dados_por_dia.items()},
                'alertas_maximos': len([c for c in todos_candidatos if c.get('score_total', 0) >= 35])
            },
            'candidatos_detalhados': todos_candidatos
        }
        
        with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Relatório de análise salvo em: {arquivo_relatorio}")
        return arquivo_relatorio

# Execução principal
if __name__ == "__main__":
    analise = AnaliseAvancada()
    analise.analisar_tendencias(7)  # Últimos 7 dias