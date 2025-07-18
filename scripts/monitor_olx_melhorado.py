#!/usr/bin/env python3
# monitor_olx_melhorado.py - Monitoramento OLX com busca regional

import requests
import json
import re
from datetime import datetime
import time
import os
from bs4 import BeautifulSoup

class MonitorOLXRegional:
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
        }
        
        # Regiões importantes para buscar
        self.regioes_olx = [
            ('www', 'Nacional'),
            ('sp', 'São Paulo'),
            ('rj', 'Rio de Janeiro'),
            ('df', 'Distrito Federal'),
            ('mg', 'Minas Gerais'),
            ('pr', 'Paraná'),
            ('rs', 'Rio Grande do Sul'),
            ('ba', 'Bahia'),
            ('sc', 'Santa Catarina'),
            ('go', 'Goiás')
        ]
    
    def gerar_termos_olx(self):
        """Termos específicos para busca na OLX"""
        return [
            "ASUS ROG Zephyrus M16",
            "ROG M16 AniMe Matrix", 
            "Zephyrus GU604",
            "ASUS ROG 16 240Hz",
            "notebook AniMe Matrix",
            "ROG Mini LED",
            "ASUS GU604",
            "Zephyrus 2023"
        ]
    
    def buscar_olx_regional(self):
        """Busca anúncios na OLX em todas as regiões"""
        resultados_todos = []
        
        for regiao, nome_regiao in self.regioes_olx:
            print(f"\n🗺️ Buscando em {nome_regiao} ({regiao}.olx.com.br)...")
            
            for termo in self.gerar_termos_olx():
                print(f"  🔍 Termo: '{termo}'")
                
                # URL específica da região
                url = f"https://{regiao}.olx.com.br/informatica/notebooks-netbooks"
                params = {
                    'q': termo,
                    'sf': '1'  # Ordenar por mais recentes
                }
                
                try:
                    response = requests.get(url, headers=self.headers, params=params, timeout=15)
                    
                    if response.status_code == 200:
                        anuncios = self.extrair_anuncios_olx(response.text, termo, regiao, nome_regiao)
                        resultados_todos.extend(anuncios)
                        print(f"    ✅ {len(anuncios)} anúncios encontrados")
                    else:
                        print(f"    ❌ Erro HTTP {response.status_code}")
                    
                    time.sleep(2)  # Evitar bloqueio
                    
                except Exception as e:
                    print(f"    ❌ Erro: {e}")
        
        return self.filtrar_candidatos_olx(resultados_todos)
    
    def extrair_anuncios_olx(self, html, termo_busca, regiao, nome_regiao):
        """Extrai anúncios do HTML da OLX"""
        anuncios = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procurar por containers de anúncios (estrutura pode mudar)
            containers = (soup.find_all('div', {'data-ds-component': True}) or
                         soup.find_all('div', class_=re.compile(r'product|item|card')) or
                         soup.find_all('li', class_=re.compile(r'product|item')))
            
            for container in containers:
                try:
                    # Extrair título
                    titulo_elem = (container.find('h2') or 
                                 container.find('h3') or
                                 container.find('a', class_=re.compile(r'title|name')))
                    titulo = titulo_elem.get_text(strip=True) if titulo_elem else ""
                    
                    # Extrair preço
                    preco_elem = (container.find('span', text=re.compile(r'R\$')) or
                                container.find('span', class_=re.compile(r'price')) or
                                container.find('p', class_=re.compile(r'price')))
                    preco_str = preco_elem.get_text(strip=True) if preco_elem else "R$ 0"
                    
                    # Extrair link
                    link_elem = container.find('a', href=True)
                    link = link_elem['href'] if link_elem else ""
                    
                    # Extrair localização
                    local_elem = container.find('span', class_=re.compile(r'location|city'))
                    localizacao = local_elem.get_text(strip=True) if local_elem else nome_regiao
                    
                    # Verificar se tem dados válidos
                    if titulo and any(word in titulo.lower() for word in ['asus', 'rog', 'notebook', 'laptop']):
                        preco = self.extrair_preco_numerico(preco_str)
                        
                        anuncio = {
                            'titulo': titulo,
                            'preco': preco,
                            'preco_str': preco_str,
                            'url': f"https://{regiao}.olx.com.br{link}" if link.startswith('/') else link,
                            'site': 'OLX',
                            'regiao': nome_regiao,
                            'regiao_codigo': regiao,
                            'localizacao': localizacao,
                            'termo_busca': termo_busca,
                            'data_busca': datetime.now().isoformat()
                        }
                        anuncios.append(anuncio)
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"    ⚠️ Erro ao processar HTML: {e}")
        
        return anuncios
    
    def extrair_preco_numerico(self, preco_str):
        """Converte string de preço para número"""
        numeros = re.findall(r'\d+', preco_str.replace('.', '').replace(',', ''))
        return int(''.join(numeros)) if numeros else 0
    
    def calcular_score_olx(self, titulo, descricao=""):
        """Calcula score específico para OLX"""
        texto_completo = (titulo + " " + descricao).lower()
        score = 0
        caracteristicas_encontradas = []
        
        # Características super específicas - PESO MAIOR
        if "anime matrix" in texto_completo:
            score += 20
            caracteristicas_encontradas.append("🎯 AniMe Matrix")
        
        if "gu604" in texto_completo:
            score += 20
            caracteristicas_encontradas.append("🎯 GU604")
        
        if "mini led" in texto_completo:
            score += 15
            caracteristicas_encontradas.append("🎯 Mini LED")
        
        # Características importantes
        if "240hz" in texto_completo:
            score += 10
            caracteristicas_encontradas.append("⭐ 240Hz")
        
        if "2560x1600" in texto_completo or "2560 x 1600" in texto_completo or "qhd" in texto_completo:
            score += 10
            caracteristicas_encontradas.append("⭐ Resolução QHD")
        
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
        
        # Hardware específico
        if "rtx 4070" in texto_completo or "rtx 4080" in texto_completo:
            score += 12
            caracteristicas_encontradas.append("🎮 RTX 40xx")
        
        if "ryzen 9" in texto_completo:
            score += 10
            caracteristicas_encontradas.append("⚡ Ryzen 9")
        
        if "32gb" in texto_completo:
            score += 8
            caracteristicas_encontradas.append("💾 32GB RAM")
        
        return score, caracteristicas_encontradas
    
    def analisar_suspeita_preco_olx(self, preco):
        """Análise específica de preço para OLX"""
        if preco < 1500:
            return "🚨 EXTREMAMENTE SUSPEITO", 15
        elif preco < 3000:
            return "🚨 MUITO SUSPEITO", 12
        elif preco < 5500:
            return "⚠️ SUSPEITO", 8
        elif preco < 8000:
            return "⚠️ PREÇO BAIXO", 5
        elif preco < 12000:
            return "💰 PREÇO RAZOÁVEL", 2
        else:
            return "💰 PREÇO ALTO", 0
    
    def filtrar_candidatos_olx(self, anuncios):
        """Filtra e pontua candidatos da OLX"""
        candidatos = []
        
        for anuncio in anuncios:
            score, caracteristicas = self.calcular_score_olx(anuncio['titulo'])
            preco = anuncio['preco']
            suspeita_preco, score_preco = self.analisar_suspeita_preco_olx(preco)
            
            score_total = score + score_preco
            
            # Filtro: só candidatos com score significativo
            if score >= 10 or score_preco >= 8:
                anuncio.update({
                    'score_similaridade': score,
                    'score_preco': score_preco,
                    'score_total': score_total,
                    'caracteristicas_encontradas': caracteristicas,
                    'suspeita_preco': suspeita_preco,
                    'nivel_alerta': self.definir_nivel_alerta_olx(score_total),
                    'probabilidade_match': self.calcular_probabilidade(score_total)
                })
                candidatos.append(anuncio)
        
        return sorted(candidatos, key=lambda x: x['score_total'], reverse=True)
    
    def definir_nivel_alerta_olx(self, score_total):
        """Define nível de alerta para OLX"""
        if score_total >= 50:
            return "🚨 ALERTA MÁXIMO"
        elif score_total >= 40:
            return "🚨 ALERTA CRÍTICO"
        elif score_total >= 30:
            return "⚠️ ALERTA ALTO"
        elif score_total >= 20:
            return "⚠️ ALERTA MÉDIO"
        else:
            return "ℹ️ MONITORAR"
    
    def calcular_probabilidade(self, score_total):
        """Calcula probabilidade em % de ser o notebook"""
        if score_total >= 55:
            return "95%+"
        elif score_total >= 45:
            return "85-95%"
        elif score_total >= 35:
            return "70-85%"
        elif score_total >= 25:
            return "50-70%"
        else:
            return "< 50%"
    
    def salvar_resultados_olx(self, candidatos):
        """Salva resultados em arquivo JSON"""
        if not candidatos:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.expanduser("~/monitor_asus_rog")
        filename = f"{base_dir}/resultados/olx_regional_candidatos_{timestamp}.json"
        
        os.makedirs(f"{base_dir}/resultados", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=2, ensure_ascii=False)
        
        return filename

# Execução principal
if __name__ == "__main__":
    print("🔍 === MONITOR OLX REGIONAL ESPECIALIZADO ===")
    print(f"⏰ Iniciando busca - {datetime.now()}")
    print("🗺️ Buscando em TODAS as regiões do Brasil")
    
    monitor = MonitorOLXRegional()
    candidatos = monitor.buscar_olx_regional()
    
    if candidatos:
        print(f"\n🎯 ENCONTRADOS {len(candidatos)} CANDIDATOS TOTAIS:")
        print("=" * 70)
        
        for i, candidato in enumerate(candidatos, 1):
            print(f"\n{i}. {candidato['nivel_alerta']} (Probabilidade: {candidato['probabilidade_match']})")
            print(f"   📝 Título: {candidato['titulo']}")
            print(f"   💰 Preço: R$ {candidato['preco']:,} ({candidato['suspeita_preco']})")
            print(f"   📊 Score: {candidato['score_total']} (Características: {candidato['score_similaridade']}, Preço: {candidato['score_preco']})")
            print(f"   ✅ Características: {', '.join(candidato['caracteristicas_encontradas'])}")
            print(f"   🗺️ Região: {candidato['regiao']} - {candidato['localizacao']}")
            print(f"   🌐 URL: {candidato['url']}")
        
        # Salvar resultados
        arquivo = monitor.salvar_resultados_olx(candidatos)
        if arquivo:
            print(f"\n💾 Resultados salvos em: {arquivo}")
        
        # Alertas críticos por região
        alertas_criticos = [c for c in candidatos if c['score_total'] >= 40]
        if alertas_criticos:
            print(f"\n🚨 {len(alertas_criticos)} ALERTAS CRÍTICOS ENCONTRADOS!")
            print("⚠️ INVESTIGAR IMEDIATAMENTE!")
            
            # Agrupar por região
            por_regiao = {}
            for alerta in alertas_criticos:
                regiao = alerta['regiao']
                if regiao not in por_regiao:
                    por_regiao[regiao] = []
                por_regiao[regiao].append(alerta)
            
            print("\n📍 Alertas por região:")
            for regiao, alertas in por_regiao.items():
                print(f"   🗺️ {regiao}: {len(alertas)} alertas críticos")
            
    else:
        print("\n✅ Nenhum candidato encontrado em nenhuma região.")
        print("🔄 Próxima verificação recomendada em 2-4 horas.") 