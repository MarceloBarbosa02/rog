#!/usr/bin/env python3
# monitor_enjoei.py - Monitoramento específico para Enjoei (usados)

import requests
import json
import re
from datetime import datetime
import time
import os
from bs4 import BeautifulSoup

class MonitorEnjoeiEspecializado:
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
    
    def gerar_termos_enjoei(self):
        """Termos específicos para busca no Enjoei"""
        return [
            "ASUS ROG Zephyrus M16",
            "ROG M16 AniMe Matrix",
            "Zephyrus GU604",
            "ASUS ROG 16 notebook",
            "notebook gamer AniMe Matrix",
            "ROG Mini LED",
            "ASUS GU604"
        ]
    
    def buscar_enjoei(self):
        """Busca anúncios no Enjoei"""
        resultados_todos = []
        
        for termo in self.gerar_termos_enjoei():
            print(f"🔍 Buscando Enjoei: '{termo}'")
            
            # URL do Enjoei para busca
            url = "https://www.enjoei.com.br/busca"
            params = {
                'q': termo,
                'ordenacao': 'recentes'
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    anuncios = self.extrair_anuncios_enjoei(response.text, termo)
                    resultados_todos.extend(anuncios)
                else:
                    print(f"❌ Erro HTTP {response.status_code} para '{termo}'")
                
                time.sleep(4)  # Enjoei pode ser sensível a muitas requests
                
            except Exception as e:
                print(f"❌ Erro na busca Enjoei '{termo}': {e}")
        
        return self.filtrar_candidatos_enjoei(resultados_todos)
    
    def extrair_anuncios_enjoei(self, html, termo_busca):
        """Extrai anúncios do HTML do Enjoei"""
        anuncios = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Enjoei usa estrutura específica para produtos
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
                    
                    # Extrair localização do vendedor
                    local_elem = container.find('span', class_=re.compile(r'location|city'))
                    localizacao = local_elem.get_text(strip=True) if local_elem else ""
                    
                    # Verificar se tem dados válidos
                    if titulo and any(word in titulo.lower() for word in ['asus', 'rog', 'notebook', 'laptop']):
                        preco = self.extrair_preco_numerico(preco_str)
                        
                        anuncio = {
                            'titulo': titulo,
                            'preco': preco,
                            'preco_str': preco_str,
                            'url': f"https://www.enjoei.com.br{link}" if link.startswith('/') else link,
                            'site': 'Enjoei',
                            'localizacao': localizacao,
                            'termo_busca': termo_busca,
                            'data_busca': datetime.now().isoformat()
                        }
                        anuncios.append(anuncio)
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"❌ Erro ao processar HTML Enjoei: {e}")
            
        # Se não conseguir pelo scraping normal, tentar método alternativo
        if not anuncios:
            anuncios = self.metodo_alternativo_enjoei(html, termo_busca)
        
        return anuncios
    
    def metodo_alternativo_enjoei(self, html, termo_busca):
        """Método alternativo para extrair dados do Enjoei"""
        anuncios = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procurar por elementos com estrutura alternativa do Enjoei
            produtos = soup.find_all('div', {'data-testid': re.compile(r'product')})
            
            if not produtos:
                produtos = soup.find_all('div', class_=re.compile(r'card|item'))
            
            for produto in produtos:
                try:
                    # Buscar título em diferentes estruturas
                    titulo = ""
                    for tag in ['h3', 'h2', 'span', 'p', 'a']:
                        titulo_elem = produto.find(tag, class_=re.compile(r'title|name'))
                        if titulo_elem:
                            titulo = titulo_elem.get_text(strip=True)
                            break
                    
                    if titulo and any(word in titulo.lower() for word in ['asus', 'rog']):
                        # Buscar preço
                        preco_str = "R$ 0"
                        for tag in ['span', 'div', 'p']:
                            preco_elem = produto.find(tag, class_=re.compile(r'price|valor'))
                            if preco_elem:
                                preco_str = preco_elem.get_text(strip=True)
                                break
                        
                        preco = self.extrair_preco_numerico(preco_str)
                        
                        # Buscar link
                        link = ""
                        link_elem = produto.find('a', href=True)
                        if link_elem:
                            link = link_elem['href']
                        
                        anuncio = {
                            'titulo': titulo,
                            'preco': preco,
                            'preco_str': preco_str,
                            'url': f"https://www.enjoei.com.br{link}" if link.startswith('/') else link,
                            'site': 'Enjoei',
                            'localizacao': '',
                            'termo_busca': termo_busca,
                            'data_busca': datetime.now().isoformat()
                        }
                        anuncios.append(anuncio)
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Método alternativo Enjoei falhou: {e}")
        
        return anuncios
    
    def extrair_preco_numerico(self, preco_str):
        """Converte string de preço para número"""
        numeros = re.findall(r'\d+', preco_str.replace('.', '').replace(',', ''))
        return int(''.join(numeros)) if numeros else 0
    
    def calcular_score_enjoei(self, titulo, descricao=""):
        """Calcula score específico para Enjoei (usados)"""
        texto_completo = (titulo + " " + descricao).lower()
        score = 0
        caracteristicas_encontradas = []
        
        # Características super específicas - PESO MAIOR para usados
        if "anime matrix" in texto_completo:
            score += 20  # Peso maior - muito específico para usados
            caracteristicas_encontradas.append("🎯 AniMe Matrix")
        
        if "gu604" in texto_completo:
            score += 20  # Peso maior - código específico
            caracteristicas_encontradas.append("🎯 GU604")
        
        if "mini led" in texto_completo:
            score += 15  # Característica única
            caracteristicas_encontradas.append("🎯 Mini LED")
        
        # Características importantes
        if "240hz" in texto_completo:
            score += 10
            caracteristicas_encontradas.append("⭐ 240Hz")
        
        if "2560x1600" in texto_completo or "2560 x 1600" in texto_completo:
            score += 10
            caracteristicas_encontradas.append("⭐ Resolução")
        
        if "2023" in texto_completo:
            score += 8
            caracteristicas_encontradas.append("⭐ 2023")
        
        # Modelo e marca
        if "zephyrus m16" in texto_completo:
            score += 15
            caracteristicas_encontradas.append("🎯 Zephyrus M16")
        
        if "asus" in texto_completo and "rog" in texto_completo:
            score += 10
            caracteristicas_encontradas.append("✓ ASUS ROG")
        
        # Penalizações para termos suspeitos em usados
        if any(termo in texto_completo for termo in ['novo', 'lacrado', 'nunca usado']):
            score -= 5  # Suspeito se está "novo" sendo vendido como usado
            caracteristicas_encontradas.append("⚠️ Anunciado como 'novo'")
        
        return score, caracteristicas_encontradas
    
    def analisar_suspeita_preco_enjoei(self, preco):
        """Análise específica de preço para Enjoei (mercado de usados)"""
        # Preços mais baixos são esperados em usados, mas ainda assim suspeitos se muito baixos
        if preco < 1000:
            return "🚨 EXTREMAMENTE SUSPEITO", 15  # Peso maior para muito baixo
        elif preco < 2500:
            return "🚨 MUITO SUSPEITO", 12
        elif preco < 4500:
            return "⚠️ SUSPEITO", 8
        elif preco < 7000:
            return "⚠️ PREÇO BAIXO PARA USADO", 5
        elif preco < 9000:
            return "💰 PREÇO RAZOÁVEL USADO", 2
        else:
            return "💰 PREÇO ALTO PARA USADO", 0
    
    def filtrar_candidatos_enjoei(self, anuncios):
        """Filtra e pontua candidatos do Enjoei"""
        candidatos = []
        
        for anuncio in anuncios:
            score, caracteristicas = self.calcular_score_enjoei(anuncio['titulo'])
            preco = anuncio['preco']
            suspeita_preco, score_preco = self.analisar_suspeita_preco_enjoei(preco)
            
            score_total = score + score_preco
            
            # Filtro: Enjoei é crítico para usados, então threshold menor
            if score >= 10 or score_preco >= 8:
                anuncio.update({
                    'score_similaridade': score,
                    'score_preco': score_preco,
                    'score_total': score_total,
                    'caracteristicas_encontradas': caracteristicas,
                    'suspeita_preco': suspeita_preco,
                    'nivel_alerta': self.definir_nivel_alerta_enjoei(score_total),
                    'probabilidade_match': self.calcular_probabilidade(score_total),
                    'observacao': 'MERCADO DE USADOS - ALTA PRIORIDADE'
                })
                candidatos.append(anuncio)
        
        return sorted(candidatos, key=lambda x: x['score_total'], reverse=True)
    
    def definir_nivel_alerta_enjoei(self, score_total):
        """Define nível de alerta para Enjoei"""
        if score_total >= 50:
            return "🚨 ALERTA MÁXIMO - ENJOEI"
        elif score_total >= 40:
            return "🚨 ALERTA CRÍTICO - ENJOEI"
        elif score_total >= 30:
            return "⚠️ ALERTA ALTO - ENJOEI"
        elif score_total >= 20:
            return "⚠️ ALERTA MÉDIO - ENJOEI"
        else:
            return "ℹ️ MONITORAR - ENJOEI"
    
    def calcular_probabilidade(self, score_total):
        """Calcula probabilidade em % de ser o notebook"""
        if score_total >= 55:
            return "98%+"
        elif score_total >= 45:
            return "90-98%"
        elif score_total >= 35:
            return "75-90%"
        elif score_total >= 25:
            return "50-75%"
        else:
            return "< 50%"
    
    def salvar_resultados_enjoei(self, candidatos):
        """Salva resultados em arquivo JSON"""
        if not candidatos:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.expanduser("~/monitor_asus_rog")
        filename = f"{base_dir}/resultados/enjoei_candidatos_{timestamp}.json"
        
        os.makedirs(f"{base_dir}/resultados", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=2, ensure_ascii=False)
        
        return filename

# Execução principal
if __name__ == "__main__":
    print("🔍 === MONITOR ENJOEI ESPECIALIZADO (USADOS) ===")
    print(f"⏰ Iniciando busca Enjoei - {datetime.now()}")
    print("🎯 FOCO: Mercado de usados - Alta prioridade para notebooks roubados")
    
    monitor = MonitorEnjoeiEspecializado()
    candidatos = monitor.buscar_enjoei()
    
    if candidatos:
        print(f"\n🎯 ENCONTRADOS {len(candidatos)} CANDIDATOS NO ENJOEI:")
        print("=" * 60)
        
        for i, candidato in enumerate(candidatos, 1):
            print(f"\n{i}. {candidato['nivel_alerta']} (Probabilidade: {candidato['probabilidade_match']})")
            print(f"   📝 Título: {candidato['titulo']}")
            print(f"   💰 Preço: R$ {candidato['preco']:,} ({candidato['suspeita_preco']})")
            print(f"   📊 Score: {candidato['score_total']} (Sim: {candidato['score_similaridade']}, Preço: {candidato['score_preco']})")
            print(f"   ✅ Características: {', '.join(candidato['caracteristicas_encontradas'])}")
            print(f"   📍 Local: {candidato.get('localizacao', 'N/A')}")
            print(f"   🌐 URL: {candidato['url']}")
            print(f"   ⚠️ {candidato['observacao']}")
        
        # Salvar resultados
        arquivo = monitor.salvar_resultados_enjoei(candidatos)
        if arquivo:
            print(f"\n💾 Resultados Enjoei salvos em: {arquivo}")
        
        # Alertas críticos - Enjoei é prioritário
        alertas_criticos = [c for c in candidatos if c['score_total'] >= 35]
        if alertas_criticos:
            print(f"\n🚨 {len(alertas_criticos)} ALERTAS CRÍTICOS NO ENJOEI!")
            print("⚠️ ENJOEI = MERCADO DE USADOS - INVESTIGAR IMEDIATAMENTE!")
            print("📋 Considerações para investigação:")
            print("   - Verificar histórico do vendedor")
            print("   - Analisar fotos (qualidade, ângulos)")
            print("   - Verificar se vendedor tem outros itens caros")
            print("   - Comparar com características específicas perdidas")
            
    else:
        print("\n✅ Nenhum candidato encontrado no Enjoei nesta varredura.")
        print("🔄 Próxima verificação recomendada em 1-2 horas (Enjoei é prioritário)")
        print("💡 Dica: Enjoei é o principal marketplace de usados - alta relevância") 