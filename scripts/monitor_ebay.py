#!/usr/bin/env python3
# monitor_ebay.py - Monitoramento específico para eBay Brasil

import requests
import json
import re
from datetime import datetime
import time
import os
from bs4 import BeautifulSoup

class MonitorEbayEspecializado:
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
    
    def buscar_ebay(self):
        """Busca anúncios no eBay Brasil"""
        resultados_todos = []
        termos = ["ASUS ROG Zephyrus M16", "ROG M16 AniMe Matrix", "Zephyrus GU604"]
        
        for termo in termos:
            print(f"🔍 Buscando eBay Brasil: '{termo}'")
            
            # eBay Brasil - usar busca web
            url = "https://www.ebay.com/sch/i.html"
            params = {
                '_nkw': termo,
                '_sacat': '0',
                'LH_PrefLoc': '3',  # Brasil
                '_sop': '10'  # Recentes primeiro
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=15)
                if response.status_code == 200:
                    anuncios = self.extrair_anuncios_ebay(response.text, termo)
                    resultados_todos.extend(anuncios)
                
                time.sleep(4)  # eBay pode ser mais sensível
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        return self.filtrar_candidatos_ebay(resultados_todos)
    
    def extrair_anuncios_ebay(self, html, termo_busca):
        """Extrai anúncios do HTML do eBay"""
        anuncios = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # eBay usa estrutura específica
            containers = (soup.find_all('div', class_=re.compile(r's-item')) or
                         soup.find_all('div', class_=re.compile(r'item')) or
                         soup.find_all('li', class_=re.compile(r's-item')))
            
            for container in containers:
                try:
                    # Título no eBay
                    titulo_elem = (container.find('h3', class_=re.compile(r's-item__title')) or
                                 container.find('h3') or
                                 container.find('a', class_=re.compile(r'title')))
                    titulo = titulo_elem.get_text(strip=True) if titulo_elem else ""
                    
                    if titulo and any(word in titulo.lower() for word in ['asus', 'rog', 'notebook', 'laptop']):
                        # Preço no eBay
                        preco_elem = (container.find('span', class_=re.compile(r's-item__price')) or
                                    container.find('span', class_=re.compile(r'price')))
                        preco_str = preco_elem.get_text(strip=True) if preco_elem else "R$ 0"
                        
                        # Converter de USD para BRL se necessário
                        preco = self.processar_preco_ebay(preco_str)
                        
                        # Link no eBay
                        link_elem = (container.find('a', class_=re.compile(r's-item__link')) or
                                   container.find('a', href=True))
                        link = link_elem['href'] if link_elem else ""
                        
                        # Localização do vendedor
                        local_elem = container.find('span', class_=re.compile(r'location|ship'))
                        localizacao = local_elem.get_text(strip=True) if local_elem else ""
                        
                        anuncio = {
                            'titulo': titulo,
                            'preco': preco,
                            'preco_str': preco_str,
                            'url': link,
                            'site': 'eBay',
                            'localizacao': localizacao,
                            'termo_busca': termo_busca,
                            'data_busca': datetime.now().isoformat()
                        }
                        anuncios.append(anuncio)
                except:
                    continue
        except Exception as e:
            print(f"❌ Erro ao processar HTML eBay: {e}")
        
        return anuncios
    
    def processar_preco_ebay(self, preco_str):
        """Processa preço do eBay (pode estar em USD)"""
        try:
            # Se tem $ mas não R$, assumir USD e converter
            if '$' in preco_str and 'R$' not in preco_str:
                numeros = re.findall(r'\d+\.?\d*', preco_str)
                if numeros:
                    preco_usd = float(numeros[0])
                    # Conversão aproximada USD -> BRL (taxa ~5.5)
                    return int(preco_usd * 5.5)
            
            # Se tem R$ ou BRL, processar normalmente
            numeros = re.findall(r'\d+', preco_str.replace('.', '').replace(',', ''))
            return int(''.join(numeros)) if numeros else 0
            
        except:
            return 0
    
    def calcular_score_ebay(self, titulo, localizacao=""):
        """Calcula score para eBay"""
        texto = (titulo + " " + localizacao).lower()
        score = 0
        caracteristicas = []
        
        # Pontuação especial para itens no Brasil
        if any(local in texto for local in ['brasil', 'brazil', 'são paulo', 'rio de janeiro']):
            score += 5
            caracteristicas.append("🇧🇷 Brasil")
        
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
    
    def analisar_suspeita_preco_ebay(self, preco):
        """Análise de preço para eBay (considerando importação)"""
        if preco < 3000:
            return "🚨 EXTREMAMENTE SUSPEITO", 15  # Muito baixo mesmo com importação
        elif preco < 5000:
            return "🚨 MUITO SUSPEITO", 12
        elif preco < 8000:
            return "⚠️ SUSPEITO", 8
        elif preco < 12000:
            return "💰 PREÇO BAIXO", 4
        elif preco < 20000:
            return "💰 PREÇO NORMAL IMPORTADO", 2
        else:
            return "💰 PREÇO ALTO", 0
    
    def filtrar_candidatos_ebay(self, anuncios):
        """Filtra candidatos do eBay"""
        candidatos = []
        
        for anuncio in anuncios:
            score, caracteristicas = self.calcular_score_ebay(anuncio['titulo'], anuncio.get('localizacao', ''))
            preco = anuncio['preco']
            suspeita_preco, score_preco = self.analisar_suspeita_preco_ebay(preco)
            
            score_total = score + score_preco
            
            if score >= 10 or score_preco >= 8:  # Threshold menor para eBay
                anuncio.update({
                    'score_similaridade': score,
                    'score_preco': score_preco,
                    'score_total': score_total,
                    'caracteristicas_encontradas': caracteristicas,
                    'suspeita_preco': suspeita_preco,
                    'nivel_alerta': self.definir_nivel_alerta(score_total),
                    'probabilidade_match': self.calcular_probabilidade(score_total),
                    'observacao': 'MERCADO INTERNACIONAL - Verificar localização'
                })
                candidatos.append(anuncio)
        
        return sorted(candidatos, key=lambda x: x['score_total'], reverse=True)
    
    def definir_nivel_alerta(self, score_total):
        """Define nível de alerta"""
        if score_total >= 45:
            return "🚨 ALERTA MÁXIMO - EBAY"
        elif score_total >= 35:
            return "⚠️ ALERTA ALTO - EBAY"
        elif score_total >= 25:
            return "⚠️ ALERTA MÉDIO - EBAY"
        else:
            return "ℹ️ MONITORAR - EBAY"
    
    def calcular_probabilidade(self, score_total):
        """Calcula probabilidade"""
        if score_total >= 50:
            return "90%+"
        elif score_total >= 40:
            return "75-90%"
        elif score_total >= 30:
            return "50-75%"
        elif score_total >= 20:
            return "25-50%"
        else:
            return "< 25%"
    
    def salvar_resultados_ebay(self, candidatos):
        """Salva resultados"""
        if not candidatos:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.expanduser("~/monitor_asus_rog")
        filename = f"{base_dir}/resultados/ebay_candidatos_{timestamp}.json"
        
        os.makedirs(f"{base_dir}/resultados", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=2, ensure_ascii=False)
        
        return filename

# Execução principal
if __name__ == "__main__":
    print("🔍 === MONITOR EBAY BRASIL ESPECIALIZADO ===")
    print(f"⏰ Iniciando busca - {datetime.now()}")
    print("🌎 FOCO: Mercado internacional - Verificar localização do vendedor")
    
    monitor = MonitorEbayEspecializado()
    candidatos = monitor.buscar_ebay()
    
    if candidatos:
        print(f"\n🎯 ENCONTRADOS {len(candidatos)} CANDIDATOS NO EBAY:")
        print("=" * 60)
        
        for i, candidato in enumerate(candidatos, 1):
            print(f"\n{i}. {candidato['nivel_alerta']} ({candidato['probabilidade_match']})")
            print(f"   📝 {candidato['titulo']}")
            print(f"   💰 R$ {candidato['preco']:,} ({candidato['suspeita_preco']})")
            print(f"   📊 Score: {candidato['score_total']}")
            print(f"   ✅ {', '.join(candidato['caracteristicas_encontradas'])}")
            print(f"   📍 Local: {candidato.get('localizacao', 'N/A')}")
            print(f"   🌐 {candidato['url']}")
            print(f"   ⚠️ {candidato['observacao']}")
        
        arquivo = monitor.salvar_resultados_ebay(candidatos)
        if arquivo:
            print(f"\n💾 Resultados salvos: {arquivo}")
        
        print(f"\n💡 DICAS PARA EBAY:")
        print("   - Verificar localização do vendedor (Brasil vs Internacional)")
        print("   - Considerar custos de importação em preços internacionais")
        print("   - Verificar reputação do vendedor")
        print("   - Analisar tempo de entrega (internacional pode ser 15-30 dias)")
            
    else:
        print("\n✅ Nenhum candidato encontrado no eBay.")
        print("💡 eBay tem menor probabilidade para itens roubados brasileiros") 