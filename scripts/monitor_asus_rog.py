#!/usr/bin/env python3
# monitor_asus_rog.py - Script principal de monitoramento

import requests
import json
import re
from datetime import datetime
import time
import os

class MonitorASUSROG:
    def __init__(self):
        self.modelo_principal = "ASUS ROG Zephyrus M16"
        self.codigo_modelo = "GU604"
        self.ano = "2023"
        self.preco_suspeito = 8000
        self.preco_muito_suspeito = 5000
        self.caracteristicas_unicas = [
            "anime matrix", "mini led", "240hz", "2560x1600", 
            "gu604", "2023", "tampa animada", "led matrix",
            "nebula hdr", "rog intelligent cooling", "rtx 4070",
            "rtx 4080", "ryzen 9", "ddr5", "32gb", "1tb ssd",
            "dolby vision", "wifi 6e", "thunderbolt 4", "qhd", 
            "16 polegadas", "zephyrus m16", "rog zephyrus",
            "gaming laptop", "keystone ii"
        ]
        
    def gerar_termos_busca(self):
        """Gera lista de termos para busca"""
        return [
            "ASUS ROG Zephyrus M16",
            "ROG Zephyrus M16 2023",
            "GU604",
            "Zephyrus M16 AniMe Matrix",
            "ROG M16 Mini LED",
            "ASUS ROG 16 240Hz",
            "notebook gamer AniMe Matrix"
        ]
    
    def calcular_score_similaridade(self, titulo, descricao=""):
        """Calcula score de similaridade com o notebook perdido"""
        texto_completo = (titulo + " " + descricao).lower()
        score = 0
        caracteristicas_encontradas = []
        
        # Pontuação por características únicas
        for caracteristica in self.caracteristicas_unicas:
            if caracteristica in texto_completo:
                if caracteristica in ["anime matrix", "gu604", "mini led"]:
                    score += 10  # Características muito específicas
                    caracteristicas_encontradas.append(f"🎯 {caracteristica}")
                elif caracteristica in ["240hz", "2560x1600", "2023"]:
                    score += 7   # Características importantes
                    caracteristicas_encontradas.append(f"⭐ {caracteristica}")
                else:
                    score += 3   # Características secundárias
                    caracteristicas_encontradas.append(f"✓ {caracteristica}")
        
        # Verificar modelo exato
        if "zephyrus m16" in texto_completo:
            score += 15
            caracteristicas_encontradas.append("🎯 Modelo Exato")
        
        # Verificar marca
        if "asus" in texto_completo and "rog" in texto_completo:
            score += 10
            caracteristicas_encontradas.append("✓ Marca/Linha")
        
        return score, caracteristicas_encontradas
    
    def analisar_suspeita_preco(self, preco):
        """Analisa se o preço é suspeito"""
        if preco < 3000:
            return "🚨 EXTREMAMENTE SUSPEITO", 10
        elif preco < 5000:
            return "⚠️ MUITO SUSPEITO", 8
        elif preco < 8000:
            return "⚠️ SUSPEITO", 5
        elif preco < 12000:
            return "💰 PREÇO BAIXO", 3
        else:
            return "💰 PREÇO NORMAL", 0

    def buscar_mercadolivre(self):
        """Busca no Mercado Livre via API"""
        resultados = []
        
        for termo in self.gerar_termos_busca()[:3]:  # Limitar para evitar bloqueio
            print(f"🔍 Buscando ML: '{termo}'")
            
            url = "https://api.mercadolibre.com/sites/MLB/search"
            params = {
                'q': termo,
                'category': 'MLB1649',  # Notebooks
                'limit': 20,
                'sort': 'date_desc'
            }
            
            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    dados = response.json()
                    
                    for item in dados.get('results', []):
                        anuncio = {
                            'titulo': item.get('title', ''),
                            'preco': item.get('price', 0),
                            'url': item.get('permalink', ''),
                            'vendedor': item.get('seller', {}).get('nickname', ''),
                            'cidade': item.get('address', {}).get('city_name', ''),
                            'data': item.get('date_created', ''),
                            'site': 'Mercado Livre',
                            'termo_busca': termo
                        }
                        
                        score, caracteristicas = self.calcular_score_similaridade(anuncio['titulo'])
                        suspeita_preco, score_preco = self.analisar_suspeita_preco(anuncio['preco'])
                        
                        if score >= 15 or score_preco >= 5:
                            anuncio.update({
                                'score_similaridade': score,
                                'score_preco': score_preco,
                                'score_total': score + score_preco,
                                'caracteristicas_encontradas': caracteristicas,
                                'suspeita_preco': suspeita_preco,
                                'nivel_alerta': self.definir_nivel_alerta(score + score_preco)
                            })
                            resultados.append(anuncio)
                
                time.sleep(2)  # Evitar bloqueio
                
            except Exception as e:
                print(f"❌ Erro ML '{termo}': {e}")
        
        return sorted(resultados, key=lambda x: x.get('score_total', 0), reverse=True)
    
    def definir_nivel_alerta(self, score_total):
        """Define nível de alerta baseado no score"""
        if score_total >= 40:
            return "🚨 ALERTA MÁXIMO"
        elif score_total >= 30:
            return "⚠️ ALERTA ALTO"
        elif score_total >= 20:
            return "⚠️ ALERTA MÉDIO"
        else:
            return "ℹ️ MONITORAR"
    
    def salvar_resultados(self, candidatos):
        """Salva resultados em arquivo JSON"""
        if not candidatos:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.expanduser("~/monitor_asus_rog")
        filename = f"{base_dir}/resultados/candidatos_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=2, ensure_ascii=False)
        
        return filename

# Script principal
if __name__ == "__main__":
    print("🔍 === MONITOR ASUS ROG ZEPHYRUS M16 ===")
    print(f"⏰ Iniciando monitoramento - {datetime.now()}")
    
    monitor = MonitorASUSROG()
    candidatos = monitor.buscar_mercadolivre()
    
    if candidatos:
        print(f"\n🎯 ENCONTRADOS {len(candidatos)} CANDIDATOS:")
        print("=" * 60)
        
        for i, candidato in enumerate(candidatos, 1):
            print(f"\n{i}. {candidato.get('nivel_alerta', 'N/A')}")
            print(f"   📝 Título: {candidato['titulo']}")
            print(f"   💰 Preço: R$ {candidato['preco']:,} ({candidato.get('suspeita_preco', '')})")
            print(f"   📊 Score: {candidato.get('score_total', 0)} (Sim: {candidato.get('score_similaridade', 0)}, Preço: {candidato.get('score_preco', 0)})")
            print(f"   ✅ Características: {', '.join(candidato.get('caracteristicas_encontradas', []))}")
            print(f"   🌐 URL: {candidato['url']}")
            print(f"   👤 Vendedor: {candidato['vendedor']} - {candidato['cidade']}")
        
        # Salvar resultados
        arquivo = monitor.salvar_resultados(candidatos)
        if arquivo:
            print(f"\n💾 Resultados salvos em: {arquivo}")
        
        # Alertas para candidatos de alto risco
        alertas_maximos = [c for c in candidatos if c.get('score_total', 0) >= 35]
        if alertas_maximos:
            print(f"\n🚨 {len(alertas_maximos)} ALERTAS MÁXIMOS ENCONTRADOS!")
            print("⚠️ VERIFICAR IMEDIATAMENTE!")
            
    else:
        print("\n✅ Nenhum candidato encontrado nesta varredura.")
        print("🔄 Próxima verificação recomendada em 2-4 horas.")