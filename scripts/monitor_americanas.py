#!/usr/bin/env python3
# monitor_americanas.py - Monitoramento específico para Americanas

import requests
import json
import re
from datetime import datetime
import time
import os
from bs4 import BeautifulSoup

class MonitorAmericanasEspecializado:
    def __init__(self):
        self.modelo_principal = "ASUS ROG Zephyrus M16"
        self.codigo_modelo = "GU604"
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
    
    def gerar_termos_americanas(self):
        """Termos específicos para busca nas Americanas"""
        return [
            "ASUS ROG Zephyrus M16",
            "ROG M16 AniMe Matrix",
            "Zephyrus GU604",
            "ASUS ROG 16 240Hz",
            "notebook AniMe Matrix"
        ]
    
    def buscar_americanas(self):
        """Busca anúncios nas Americanas"""
        resultados_todos = []
        
        for termo in self.gerar_termos_americanas():
            print(f"🔍 Buscando Americanas: '{termo}'")
            
            # URL das Americanas para busca
            url = "https://www.americanas.com.br/busca"
            params = {
                'termo': termo,
                'sortBy': 'relevance'
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    anuncios = self.extrair_anuncios_americanas(response.text, termo)
                    resultados_todos.extend(anuncios)
                else:
                    print(f"❌ Erro HTTP {response.status_code} para '{termo}'")
                
                time.sleep(3)  # Respeitar rate limit
                
            except Exception as e:
                print(f"❌ Erro na busca Americanas '{termo}': {e}")
        
        return self.filtrar_candidatos_americanas(resultados_todos)
    
    def extrair_anuncios_americanas(self, html, termo_busca):
        """Extrai anúncios do HTML das Americanas"""
        anuncios = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Americanas usa estrutura específica para produtos
            containers = (soup.find_all('div', class_=re.compile(r'product|item')) or
                         soup.find_all('article', class_=re.compile(r'product')) or
                         soup.find_all('li', class_=re.compile(r'product|item')))
            
            for container in containers:
                try:
                    # Extrair título
                    titulo_elem = (container.find('h3') or 
                                 container.find('h2') or
                                 container.find('span', class_=re.compile(r'title|name')) or
                                 container.find('a', class_=re.compile(r'title|name')))
                    titulo = titulo_elem.get_text(strip=True) if titulo_elem else ""
                    
                    # Extrair preço
                    preco_elem = (container.find('span', class_=re.compile(r'price')) or
                                container.find('div', class_=re.compile(r'price')) or
                                container.find('p', class_=re.compile(r'price')))
                    preco_str = preco_elem.get_text(strip=True) if preco_elem else "R$ 0"
                    
                    # Extrair link
                    link_elem = container.find('a', href=True)
                    link = link_elem['href'] if link_elem else ""
                    
                    # Verificar se tem dados válidos
                    if titulo and any(word in titulo.lower() for word in ['asus', 'rog', 'notebook', 'laptop']):
                        preco = self.extrair_preco_numerico(preco_str)
                        
                        anuncio = {
                            'titulo': titulo,
                            'preco': preco,
                            'preco_str': preco_str,
                            'url': f"https://www.americanas.com.br{link}" if link.startswith('/') else link,
                            'site': 'Americanas',
                            'termo_busca': termo_busca,
                            'data_busca': datetime.now().isoformat()
                        }
                        anuncios.append(anuncio)
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"❌ Erro ao processar HTML Americanas: {e}")
        
        return anuncios
    
    def extrair_preco_numerico(self, preco_str):
        """Converte string de preço para número"""
        numeros = re.findall(r'\d+', preco_str.replace('.', '').replace(',', ''))
        return int(''.join(numeros)) if numeros else 0
    
    def calcular_score_americanas(self, titulo, descricao=""):
        """Calcula score específico para Americanas"""
        texto_completo = (titulo + " " + descricao).lower()
        score = 0
        caracteristicas_encontradas = []
        
        # Características super específicas
        if "anime matrix" in texto_completo:
            score += 15
            caracteristicas_encontradas.append("🎯 AniMe Matrix")
        
        if "gu604" in texto_completo:
            score += 15
            caracteristicas_encontradas.append("🎯 GU604")
        
        if "mini led" in texto_completo:
            score += 12
            caracteristicas_encontradas.append("🎯 Mini LED")
        
        # Características importantes
        if "240hz" in texto_completo:
            score += 8
            caracteristicas_encontradas.append("⭐ 240Hz")
        
        if "2560x1600" in texto_completo or "2560 x 1600" in texto_completo:
            score += 8
            caracteristicas_encontradas.append("⭐ Resolução")
        
        if "2023" in texto_completo:
            score += 6
            caracteristicas_encontradas.append("⭐ 2023")
        
        # Modelo e marca
        if "zephyrus m16" in texto_completo:
            score += 12
            caracteristicas_encontradas.append("🎯 Zephyrus M16")
        
        if "asus" in texto_completo and "rog" in texto_completo:
            score += 8
            caracteristicas_encontradas.append("✓ ASUS ROG")
        
        return score, caracteristicas_encontradas
    
    def analisar_suspeita_preco_americanas(self, preco):
        """Análise específica de preço para Americanas"""
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
    
    def filtrar_candidatos_americanas(self, anuncios):
        """Filtra e pontua candidatos das Americanas"""
        candidatos = []
        
        for anuncio in anuncios:
            score, caracteristicas = self.calcular_score_americanas(anuncio['titulo'])
            preco = anuncio['preco']
            suspeita_preco, score_preco = self.analisar_suspeita_preco_americanas(preco)
            
            score_total = score + score_preco
            
            # Filtro: só candidatos com score significativo
            if score >= 12 or score_preco >= 7:
                anuncio.update({
                    'score_similaridade': score,
                    'score_preco': score_preco,
                    'score_total': score_total,
                    'caracteristicas_encontradas': caracteristicas,
                    'suspeita_preco': suspeita_preco,
                    'nivel_alerta': self.definir_nivel_alerta_americanas(score_total),
                    'probabilidade_match': self.calcular_probabilidade(score_total)
                })
                candidatos.append(anuncio)
        
        return sorted(candidatos, key=lambda x: x['score_total'], reverse=True)
    
    def definir_nivel_alerta_americanas(self, score_total):
        """Define nível de alerta para Americanas"""
        if score_total >= 45:
            return "🚨 ALERTA MÁXIMO"
        elif score_total >= 35:
            return "⚠️ ALERTA ALTO"
        elif score_total >= 25:
            return "⚠️ ALERTA MÉDIO"
        else:
            return "ℹ️ MONITORAR"
    
    def calcular_probabilidade(self, score_total):
        """Calcula probabilidade em % de ser o notebook"""
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
    
    def salvar_resultados_americanas(self, candidatos):
        """Salva resultados em arquivo JSON"""
        if not candidatos:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.expanduser("~/monitor_asus_rog")
        filename = f"{base_dir}/resultados/americanas_candidatos_{timestamp}.json"
        
        os.makedirs(f"{base_dir}/resultados", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=2, ensure_ascii=False)
        
        return filename

# Execução principal
if __name__ == "__main__":
    print("🔍 === MONITOR AMERICANAS ESPECIALIZADO ===")
    print(f"⏰ Iniciando busca Americanas - {datetime.now()}")
    
    monitor = MonitorAmericanasEspecializado()
    candidatos = monitor.buscar_americanas()
    
    if candidatos:
        print(f"\n🎯 ENCONTRADOS {len(candidatos)} CANDIDATOS NAS AMERICANAS:")
        print("=" * 60)
        
        for i, candidato in enumerate(candidatos, 1):
            print(f"\n{i}. {candidato['nivel_alerta']} (Probabilidade: {candidato['probabilidade_match']})")
            print(f"   📝 Título: {candidato['titulo']}")
            print(f"   💰 Preço: R$ {candidato['preco']:,} ({candidato['suspeita_preco']})")
            print(f"   📊 Score: {candidato['score_total']} (Sim: {candidato['score_similaridade']}, Preço: {candidato['score_preco']})")
            print(f"   ✅ Características: {', '.join(candidato['caracteristicas_encontradas'])}")
            print(f"   🌐 URL: {candidato['url']}")
        
        # Salvar resultados
        arquivo = monitor.salvar_resultados_americanas(candidatos)
        if arquivo:
            print(f"\n💾 Resultados Americanas salvos em: {arquivo}")
        
        # Alertas críticos
        alertas_criticos = [c for c in candidatos if c['score_total'] >= 40]
        if alertas_criticos:
            print(f"\n🚨 {len(alertas_criticos)} ALERTAS CRÍTICOS NAS AMERICANAS!")
            print("⚠️ INVESTIGAR IMEDIATAMENTE!")
            
    else:
        print("\n✅ Nenhum candidato encontrado nas Americanas nesta varredura.")
        print("🔄 Próxima verificação recomendada em 2-4 horas.") 