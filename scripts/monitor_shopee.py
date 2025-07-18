#!/usr/bin/env python3
# monitor_shopee.py - Monitoramento específico para Shopee

import requests
import json
import re
from datetime import datetime
import time
import os
from bs4 import BeautifulSoup

class MonitorShopeeEspecializado:
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
    
    def gerar_termos_shopee(self):
        """Termos específicos para busca na Shopee"""
        return [
            "ASUS ROG Zephyrus M16",
            "ROG M16 AniMe Matrix",
            "Zephyrus GU604",
            "ASUS ROG 16 240Hz",
            "notebook AniMe Matrix",
            "ROG Mini LED"
        ]
    
    def buscar_shopee(self):
        """Busca anúncios na Shopee"""
        resultados_todos = []
        
        for termo in self.gerar_termos_shopee():
            print(f"🔍 Buscando Shopee: '{termo}'")
            
            # URL da Shopee para busca
            url = "https://shopee.com.br/search"
            params = {
                'keyword': termo,
                'page': 0,
                'sortBy': 'ctime'  # Ordenar por mais recentes
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    anuncios = self.extrair_anuncios_shopee(response.text, termo)
                    resultados_todos.extend(anuncios)
                else:
                    print(f"❌ Erro HTTP {response.status_code} para '{termo}'")
                
                time.sleep(4)  # Evitar bloqueio - Shopee é mais restritiva
                
            except Exception as e:
                print(f"❌ Erro na busca Shopee '{termo}': {e}")
        
        return self.filtrar_candidatos_shopee(resultados_todos)
    
    def extrair_anuncios_shopee(self, html, termo_busca):
        """Extrai anúncios do HTML da Shopee"""
        anuncios = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Shopee usa estrutura com JSON embutido ou elementos específicos
            # Procurar por containers de produtos
            containers = soup.find_all('div', {'data-sqe': 'item'}) or soup.find_all('div', class_=re.compile(r'item|product'))
            
            for container in containers:
                try:
                    # Extrair título
                    titulo_elem = (container.find('div', {'data-sqe': 'name'}) or 
                                 container.find('span', class_=re.compile(r'title|name')) or
                                 container.find('div', class_=re.compile(r'title|name')))
                    titulo = titulo_elem.get_text(strip=True) if titulo_elem else ""
                    
                    # Extrair preço
                    preco_elem = (container.find('span', class_=re.compile(r'price')) or
                                container.find('div', class_=re.compile(r'price')))
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
                            'url': f"https://shopee.com.br{link}" if link.startswith('/') else link,
                            'site': 'Shopee',
                            'termo_busca': termo_busca,
                            'data_busca': datetime.now().isoformat()
                        }
                        anuncios.append(anuncio)
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"❌ Erro ao processar HTML Shopee: {e}")
            
        # Se não conseguir pelo scraping normal, tentar método alternativo
        if not anuncios:
            anuncios = self.metodo_alternativo_shopee(html, termo_busca)
        
        return anuncios
    
    def metodo_alternativo_shopee(self, html, termo_busca):
        """Método alternativo para extrair dados da Shopee"""
        anuncios = []
        
        try:
            # Procurar por dados JSON embutidos na página
            soup = BeautifulSoup(html, 'html.parser')
            scripts = soup.find_all('script', type='application/json')
            
            for script in scripts:
                try:
                    data = json.loads(script.get_text())
                    # Navegar pela estrutura JSON para encontrar produtos
                    # (estrutura pode variar)
                    if isinstance(data, dict) and 'items' in data:
                        for item in data['items']:
                            titulo = item.get('name', '')
                            preco = item.get('price', 0)
                            
                            if titulo and any(word in titulo.lower() for word in ['asus', 'rog']):
                                anuncio = {
                                    'titulo': titulo,
                                    'preco': preco // 100000 if preco > 100000 else preco,  # Shopee usa centavos
                                    'preco_str': f"R$ {preco // 100000}" if preco > 100000 else f"R$ {preco}",
                                    'url': f"https://shopee.com.br/item/{item.get('shopid', '')}/{item.get('itemid', '')}",
                                    'site': 'Shopee',
                                    'termo_busca': termo_busca,
                                    'data_busca': datetime.now().isoformat()
                                }
                                anuncios.append(anuncio)
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Método alternativo Shopee falhou: {e}")
        
        return anuncios
    
    def extrair_preco_numerico(self, preco_str):
        """Converte string de preço para número"""
        numeros = re.findall(r'\d+', preco_str.replace('.', '').replace(',', ''))
        return int(''.join(numeros)) if numeros else 0
    
    def calcular_score_shopee(self, titulo, descricao=""):
        """Calcula score específico para Shopee"""
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
    
    def analisar_suspeita_preco_shopee(self, preco):
        """Análise específica de preço para Shopee"""
        if preco < 1500:
            return "🚨 EXTREMAMENTE SUSPEITO", 12
        elif preco < 3500:
            return "⚠️ MUITO SUSPEITO", 10
        elif preco < 6500:
            return "⚠️ SUSPEITO", 7
        elif preco < 9000:
            return "💰 PREÇO BAIXO", 4
        else:
            return "💰 PREÇO NORMAL", 0
    
    def filtrar_candidatos_shopee(self, anuncios):
        """Filtra e pontua candidatos da Shopee"""
        candidatos = []
        
        for anuncio in anuncios:
            score, caracteristicas = self.calcular_score_shopee(anuncio['titulo'])
            preco = anuncio['preco']
            suspeita_preco, score_preco = self.analisar_suspeita_preco_shopee(preco)
            
            score_total = score + score_preco
            
            # Filtro: só candidatos com score significativo
            if score >= 12 or score_preco >= 7:
                anuncio.update({
                    'score_similaridade': score,
                    'score_preco': score_preco,
                    'score_total': score_total,
                    'caracteristicas_encontradas': caracteristicas,
                    'suspeita_preco': suspeita_preco,
                    'nivel_alerta': self.definir_nivel_alerta_shopee(score_total),
                    'probabilidade_match': self.calcular_probabilidade(score_total)
                })
                candidatos.append(anuncio)
        
        return sorted(candidatos, key=lambda x: x['score_total'], reverse=True)
    
    def definir_nivel_alerta_shopee(self, score_total):
        """Define nível de alerta para Shopee"""
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
    
    def salvar_resultados_shopee(self, candidatos):
        """Salva resultados em arquivo JSON"""
        if not candidatos:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.expanduser("~/monitor_asus_rog")
        filename = f"{base_dir}/resultados/shopee_candidatos_{timestamp}.json"
        
        os.makedirs(f"{base_dir}/resultados", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=2, ensure_ascii=False)
        
        return filename

# Execução principal
if __name__ == "__main__":
    print("🔍 === MONITOR SHOPEE ESPECIALIZADO ===")
    print(f"⏰ Iniciando busca Shopee - {datetime.now()}")
    
    monitor = MonitorShopeeEspecializado()
    candidatos = monitor.buscar_shopee()
    
    if candidatos:
        print(f"\n🎯 ENCONTRADOS {len(candidatos)} CANDIDATOS NA SHOPEE:")
        print("=" * 60)
        
        for i, candidato in enumerate(candidatos, 1):
            print(f"\n{i}. {candidato['nivel_alerta']} (Probabilidade: {candidato['probabilidade_match']})")
            print(f"   📝 Título: {candidato['titulo']}")
            print(f"   💰 Preço: R$ {candidato['preco']:,} ({candidato['suspeita_preco']})")
            print(f"   📊 Score: {candidato['score_total']} (Sim: {candidato['score_similaridade']}, Preço: {candidato['score_preco']})")
            print(f"   ✅ Características: {', '.join(candidato['caracteristicas_encontradas'])}")
            print(f"   🌐 URL: {candidato['url']}")
        
        # Salvar resultados
        arquivo = monitor.salvar_resultados_shopee(candidatos)
        if arquivo:
            print(f"\n💾 Resultados Shopee salvos em: {arquivo}")
        
        # Alertas críticos
        alertas_criticos = [c for c in candidatos if c['score_total'] >= 40]
        if alertas_criticos:
            print(f"\n🚨 {len(alertas_criticos)} ALERTAS CRÍTICOS NA SHOPEE!")
            print("⚠️ INVESTIGAR IMEDIATAMENTE!")
            
    else:
        print("\n✅ Nenhum candidato encontrado na Shopee nesta varredura.")
        print("🔄 Próxima verificação recomendada em 2-4 horas.") 