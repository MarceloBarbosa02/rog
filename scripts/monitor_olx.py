#!/usr/bin/env python3
# monitor_olx.py - Monitoramento específico para OLX

import requests
import json
import re
from datetime import datetime
import time
import os
from bs4 import BeautifulSoup

class MonitorOLXEspecializado:
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def gerar_termos_olx(self):
        """Termos específicos para busca na OLX"""
        return [
            "ASUS ROG Zephyrus M16",
            "ROG M16 AniMe Matrix",
            "Zephyrus GU604",
            "ASUS ROG 16 240Hz",
            "notebook AniMe Matrix",
            "ROG Mini LED"
        ]
    
    def buscar_olx(self):
        """Busca anúncios na OLX"""
        resultados_todos = []
        
        for termo in self.gerar_termos_olx():
            print(f"🔍 Buscando OLX: '{termo}'")
            
            # URL da OLX para notebooks
            url = f"https://www.olx.com.br/informatica/notebooks-netbooks"
            params = {
                'q': termo,
                'sf': '1'  # Ordenar por mais recentes
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    anuncios = self.extrair_anuncios_olx(response.text, termo)
                    resultados_todos.extend(anuncios)
                else:
                    print(f"❌ Erro HTTP {response.status_code} para '{termo}'")
                
                time.sleep(3)  # Evitar bloqueio
                
            except Exception as e:
                print(f"❌ Erro na busca OLX '{termo}': {e}")
        
        return self.filtrar_candidatos_olx(resultados_todos)
    
    def extrair_anuncios_olx(self, html, termo_busca):
        """Extrai anúncios do HTML da OLX"""
        anuncios = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Procurar por containers de anúncios (estrutura pode mudar)
            containers = soup.find_all('div', {'data-ds-component': True})
            
            for container in containers:
                try:
                    # Extrair título
                    titulo_elem = container.find('h2') or container.find('h3')
                    titulo = titulo_elem.get_text(strip=True) if titulo_elem else ""
                    
                    # Extrair preço
                    preco_elem = container.find('span', text=re.compile(r'R\$'))
                    preco_str = preco_elem.get_text(strip=True) if preco_elem else "R$ 0"
                    
                    # Extrair link
                    link_elem = container.find('a', href=True)
                    link = link_elem['href'] if link_elem else ""
                    
                    # Verificar se tem dados válidos
                    if titulo and any(word in titulo.lower() for word in ['asus', 'rog', 'notebook']):
                        preco = self.extrair_preco_numerico(preco_str)
                        
                        anuncio = {
                            'titulo': titulo,
                            'preco': preco,
                            'preco_str': preco_str,
                            'url': f"https://olx.com.br{link}" if link.startswith('/') else link,
                            'site': 'OLX',
                            'termo_busca': termo_busca,
                            'data_busca': datetime.now().isoformat()
                        }
                        anuncios.append(anuncio)
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"❌ Erro ao processar HTML OLX: {e}")
        
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
    
    def analisar_suspeita_preco_olx(self, preco):
        """Análise específica de preço para OLX"""
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
    
    def filtrar_candidatos_olx(self, anuncios):
        """Filtra e pontua candidatos da OLX"""
        candidatos = []
        
        for anuncio in anuncios:
            score, caracteristicas = self.calcular_score_olx(anuncio['titulo'])
            preco = anuncio['preco']
            suspeita_preco, score_preco = self.analisar_suspeita_preco_olx(preco)
            
            score_total = score + score_preco
            
            # Filtro: só candidatos com score significativo
            if score >= 12 or score_preco >= 7:
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
        if score_total >= 45:
            return "🚨 ALERTA MÁXIMO"
        elif score_total >= 35:
            return "⚠️ ALERTA ALTO"
        elif score_total >= 25:
            return "⚠️ ALERTA MÉDIO"
        else:
            return "ℹ️ MONITORAR"
    
    def calcular_probabilidade(self, score_total):
        """Calcula probabilidade de match"""
        if score_total >= 45:
            return "95%+"
        elif score_total >= 35:
            return "80-95%"
        elif score_total >= 25:
            return "60-80%"
        else:
            return "30-60%"
    
    def salvar_resultados_olx(self, candidatos):
        """Salva resultados específicos da OLX"""
        if not candidatos:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.expanduser("~/monitor_asus_rog")
        filename = f"{base_dir}/resultados/olx_candidatos_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(candidatos, f, indent=2, ensure_ascii=False)
        
        return filename

# Execução principal
if __name__ == "__main__":
    print("🔍 === MONITOR OLX ESPECIALIZADO ===")
    print(f"⏰ Iniciando busca OLX - {datetime.now()}")
    
    monitor = MonitorOLXEspecializado()
    candidatos = monitor.buscar_olx()
    
    if candidatos:
        print(f"\n🎯 ENCONTRADOS {len(candidatos)} CANDIDATOS NA OLX:")
        print("=" * 60)
        
        for i, candidato in enumerate(candidatos, 1):
            print(f"\n{i}. {candidato['nivel_alerta']} (Probabilidade: {candidato['probabilidade_match']})")
            print(f"   📝 Título: {candidato['titulo']}")
            print(f"   💰 Preço: R$ {candidato['preco']:,} ({candidato['suspeita_preco']})")
            print(f"   📊 Score: {candidato['score_total']} (Sim: {candidato['score_similaridade']}, Preço: {candidato['score_preco']})")
            print(f"   ✅ Características: {', '.join(candidato['caracteristicas_encontradas'])}")
            print(f"   🌐 URL: {candidato['url']}")
        
        # Salvar resultados
        arquivo = monitor.salvar_resultados_olx(candidatos)
        if arquivo:
            print(f"\n💾 Resultados OLX salvos em: {arquivo}")
        
        # Alertas críticos
        alertas_criticos = [c for c in candidatos if c['score_total'] >= 40]
        if alertas_criticos:
            print(f"\n🚨 {len(alertas_criticos)} ALERTAS CRÍTICOS NA OLX!")
            print("⚠️ INVESTIGAR IMEDIATAMENTE!")
            
    else:
        print("\n✅ Nenhum candidato encontrado na OLX nesta varredura.")
        