#!/usr/bin/env python3
# monitor_pontofrio.py - Monitoramento específico para Ponto Frio

import requests
import json
import re
from datetime import datetime
import time
import os
from bs4 import BeautifulSoup

class MonitorPontoFrioEspecializado:
    def __init__(self):
        self.caracteristicas_unicas = [
            "anime matrix", "mini led", "240hz", "2560x1600", 
            "gu604", "2023", "tampa animada", "led matrix",
            "nebula hdr", "rog intelligent cooling", "rtx 4070",
            "rtx 4080", "ryzen 9", "ddr5", "32gb", "1tb ssd",
            "dolby vision", "wifi 6e", "thunderbolt 4", "qhd", 
            "16 polegadas", "zephyrus m16", "rog zephyrus",
            "gaming laptop", "keystone ii"
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def buscar_pontofrio(self):
        """Busca anúncios no Ponto Frio"""
        resultados_todos = []
        termos = ["ASUS ROG Zephyrus M16", "ROG M16 AniMe Matrix", "Zephyrus GU604"]
        
        for termo in termos:
            print(f"🔍 Buscando Ponto Frio: '{termo}'")
            
            url = "https://www.pontofrio.com.br/busca"
            params = {'q': termo}
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=15)
                if response.status_code == 200:
                    anuncios = self.extrair_anuncios_pontofrio(response.text, termo)
                    resultados_todos.extend(anuncios)
                
                time.sleep(3)
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        return self.filtrar_candidatos_pontofrio(resultados_todos)
    
    def extrair_anuncios_pontofrio(self, html, termo_busca):
        """Extrai anúncios do HTML do Ponto Frio"""
        anuncios = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            containers = soup.find_all('div', class_=re.compile(r'product|item'))
            
            for container in containers:
                try:
                    titulo_elem = container.find(['h3', 'h2', 'span'], class_=re.compile(r'title|name'))
                    titulo = titulo_elem.get_text(strip=True) if titulo_elem else ""
                    
                    if titulo and any(word in titulo.lower() for word in ['asus', 'rog', 'notebook']):
                        preco_elem = container.find(['span', 'div'], class_=re.compile(r'price'))
                        preco_str = preco_elem.get_text(strip=True) if preco_elem else "R$ 0"
                        preco = self.extrair_preco_numerico(preco_str)
                        
                        link_elem = container.find('a', href=True)
                        link = link_elem['href'] if link_elem else ""
                        
                        anuncio = {
                            'titulo': titulo,
                            'preco': preco,
                            'preco_str': preco_str,
                            'url': f"https://www.pontofrio.com.br{link}" if link.startswith('/') else link,
                            'site': 'Ponto Frio',
                            'termo_busca': termo_busca,
                            'data_busca': datetime.now().isoformat()
                        }
                        anuncios.append(anuncio)
                except:
                    continue
        except Exception as e:
            print(f"❌ Erro ao processar HTML: {e}")
        
        return anuncios
    
    def extrair_preco_numerico(self, preco_str):
        """Converte string de preço para número"""
        numeros = re.findall(r'\d+', preco_str.replace('.', '').replace(',', ''))
        return int(''.join(numeros)) if numeros else 0
    
    def calcular_score_pontofrio(self, titulo):
        """Calcula score para Ponto Frio"""
        texto = titulo.lower()
        score = 0
        caracteristicas = []
        
        if "anime matrix" in texto:
            score += 15
            caracteristicas.append("🎯 AniMe Matrix")
        if "gu604" in texto:
            score += 15
            caracteristicas.append("🎯 GU604")
        if "mini led" in texto:
            score += 12
            caracteristicas.append("🎯 Mini LED")
        if "240hz" in texto:
            score += 8
            caracteristicas.append("⭐ 240Hz")
        if "zephyrus m16" in texto:
            score += 12
            caracteristicas.append("🎯 Zephyrus M16")
        if "asus" in texto and "rog" in texto:
            score += 8
            caracteristicas.append("✓ ASUS ROG")
        
        return score, caracteristicas
    
    def analisar_suspeita_preco_pontofrio(self, preco):
        """Análise de preço para Ponto Frio"""
        if preco < 2000:
            return "🚨 EXTREMAMENTE SUSPEITO", 12
        elif preco < 4000:
            return "⚠️ MUITO SUSPEITO", 10
        elif preco < 7000:
            return "⚠️ SUSPEITO", 7
        elif preco < 10000:
            return "💰 PREÇO BAIXO", 4
        else:
            return "💰 PREÇO NORMAL", 0
    
    def filtrar_candidatos_pontofrio(self, anuncios):
        """Filtra candidatos do Ponto Frio"""
        candidatos = []
        
        for anuncio in anuncios:
            score, caracteristicas = self.calcular_score_pontofrio(anuncio['titulo'])
            preco = anuncio['preco']
            suspeita_preco, score_preco = self.analisar_suspeita_preco_pontofrio(preco)
            
            score_total = score + score_preco
            
            if score >= 12 or score_preco >= 7:
                anuncio.update({
                    'score_similaridade': score,
                    'score_preco': score_preco,
                    'score_total': score_total,
                    'caracteristicas_encontradas': caracteristicas,
                    'suspeita_preco': suspeita_preco,
                    'nivel_alerta': self.definir_nivel_alerta(score_total),
                    'probabilidade_match': self.calcular_probabilidade(score_total)
                })
                candidatos.append(anuncio)
        
        return sorted(candidatos, key=lambda x: x['score_total'], reverse=True)
    
    def definir_nivel_alerta(self, score_total):
        """Define nível de alerta"""
        if score_total >= 45:
            return "🚨 ALERTA MÁXIMO"
        elif score_total >= 35:
            return "⚠️ ALERTA ALTO"
        elif score_total >= 25:
            return "⚠️ ALERTA MÉDIO"
        else:
            return "ℹ️ MONITORAR"
    
    def calcular_probabilidade(self, score_total):
        """Calcula probabilidade"""
        if score_total >= 50:
            return "95%+"
        elif score_total >= 40:
            return "80-95%"
        elif score_total >= 30:
            return "60-80%"
        elif score_total >= 20:
            return "40-60%"
        else:
            return "< 40%"
    
    def salvar_resultados_pontofrio(self, candidatos):
        """Salva resultados"""
        if not candidatos:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.expanduser("~/monitor_asus_rog")
        filename = f"{base_dir}/resultados/pontofrio_candidatos_{timestamp}.json"
        
        os.makedirs(f"{base_dir}/resultados", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=2, ensure_ascii=False)
        
        return filename

# Execução principal
if __name__ == "__main__":
    print("🔍 === MONITOR PONTO FRIO ESPECIALIZADO ===")
    print(f"⏰ Iniciando busca - {datetime.now()}")
    
    monitor = MonitorPontoFrioEspecializado()
    candidatos = monitor.buscar_pontofrio()
    
    if candidatos:
        print(f"\n🎯 ENCONTRADOS {len(candidatos)} CANDIDATOS:")
        print("=" * 60)
        
        for i, candidato in enumerate(candidatos, 1):
            print(f"\n{i}. {candidato['nivel_alerta']} ({candidato['probabilidade_match']})")
            print(f"   📝 {candidato['titulo']}")
            print(f"   💰 R$ {candidato['preco']:,} ({candidato['suspeita_preco']})")
            print(f"   📊 Score: {candidato['score_total']}")
            print(f"   ✅ {', '.join(candidato['caracteristicas_encontradas'])}")
            print(f"   🌐 {candidato['url']}")
        
        arquivo = monitor.salvar_resultados_pontofrio(candidatos)
        if arquivo:
            print(f"\n💾 Resultados salvos: {arquivo}")
            
    else:
        print("\n✅ Nenhum candidato encontrado.") 