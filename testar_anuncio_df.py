#!/usr/bin/env python3
# testar_anuncio_df.py - Teste específico do anúncio do DF

import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

def testar_anuncio_especifico():
    """Testa o anúncio específico do DF"""
    url = "https://df.olx.com.br/distrito-federal-e-regiao/informatica/notebooks/notebook-gamer-asus-rog-zephyrus-1420467003"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
    }
    
    print(f"🔍 Testando anúncio específico do DF...")
    print(f"🌐 URL: {url}")
    print()
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"📡 Status HTTP: {response.status_code}")
        print(f"📄 Tamanho da resposta: {len(response.text)} caracteres")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar título
            titulo_elem = soup.find('h1')
            titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Título não encontrado"
            
            # Buscar preço
            preco = "Preço não encontrado"
            preco_elem = soup.find('span', class_=re.compile(r'price|valor'))
            if preco_elem:
                preco = preco_elem.get_text(strip=True)
            else:
                # Busca alternativa por texto
                preco_text = soup.find(text=re.compile(r'R\$'))
                if preco_text:
                    preco = str(preco_text).strip()
            
            # Buscar descrição
            desc_elem = soup.find('div', class_=re.compile(r'description|desc'))
            descricao = desc_elem.get_text(strip=True)[:200] + "..." if desc_elem else "Descrição não encontrada"
            
            print(f"✅ Anúncio encontrado!")
            print(f"📝 Título: {titulo}")
            print(f"💰 Preço: {preco}")
            print(f"📄 Descrição: {descricao}")
            print()
            
            # Analisar características específicas
            texto_completo = (titulo + " " + descricao).lower()
            
            print("🎯 ANÁLISE DE CARACTERÍSTICAS:")
            caracteristicas_encontradas = []
            score = 0
            
            # Características super específicas
            if "anime matrix" in texto_completo:
                score += 20
                caracteristicas_encontradas.append("🎯 AniMe Matrix")
            
            if "gu604" in texto_completo:
                score += 20
                caracteristicas_encontradas.append("🎯 GU604")
            
            if "mini led" in texto_completo:
                score += 15
                caracteristicas_encontradas.append("🎯 Mini LED")
            
            if "240hz" in texto_completo:
                score += 10
                caracteristicas_encontradas.append("⭐ 240Hz")
            
            if "2560x1600" in texto_completo or "2560 x 1600" in texto_completo:
                score += 10
                caracteristicas_encontradas.append("⭐ Resolução QHD")
            
            if "2023" in texto_completo:
                score += 8
                caracteristicas_encontradas.append("⭐ 2023")
            
            if "zephyrus m16" in texto_completo:
                score += 15
                caracteristicas_encontradas.append("🎯 Zephyrus M16")
            
            if "asus" in texto_completo and "rog" in texto_completo:
                score += 10
                caracteristicas_encontradas.append("✓ ASUS ROG")
            
            # Características técnicas
            if "rtx 4070" in texto_completo or "rtx 4080" in texto_completo:
                score += 12
                caracteristicas_encontradas.append("🎮 RTX 40xx")
            
            if "ryzen 9" in texto_completo:
                score += 10
                caracteristicas_encontradas.append("⚡ Ryzen 9")
            
            if "32gb" in texto_completo:
                score += 8
                caracteristicas_encontradas.append("💾 32GB RAM")
            
            print(f"📊 Score Total: {score}")
            if caracteristicas_encontradas:
                print(f"✅ Características encontradas: {', '.join(caracteristicas_encontradas)}")
            else:
                print("❌ Nenhuma característica específica encontrada")
            
            # Análise de preço
            try:
                numeros = re.findall(r'\d+', preco.replace('.', '').replace(',', ''))
                preco_numerico = int(''.join(numeros)) if numeros else 0
                
                if preco_numerico > 0:
                    print()
                    if preco_numerico < 2000:
                        print("🚨 PREÇO EXTREMAMENTE SUSPEITO!")
                    elif preco_numerico < 4000:
                        print("⚠️ PREÇO MUITO SUSPEITO!")
                    elif preco_numerico < 7000:
                        print("⚠️ PREÇO SUSPEITO!")
                    else:
                        print("💰 Preço dentro do esperado para usados")
            except:
                print("❌ Não foi possível analisar o preço")
            
            print()
            print("🤔 POR QUE O SCRIPT NÃO ENCONTROU:")
            print("1. 🌍 Busca só em www.olx.com.br (nacional)")
            print("2. 📍 Este anúncio está em df.olx.com.br (regional)")
            print("3. 🔍 Termos de busca podem não bater exatamente")
            print("4. ⏰ Anúncio pode ser muito recente")
            
        elif response.status_code == 404:
            print("❌ Anúncio não encontrado (404) - pode ter sido removido")
        else:
            print(f"❌ Erro HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def testar_busca_df():
    """Testa busca geral no DF"""
    print("\n🔍 Testando busca geral no DF...")
    
    url = "https://df.olx.com.br/informatica/notebooks-netbooks"
    params = {'q': 'ASUS ROG Zephyrus'}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            print(f"✅ Busca no DF funcionando! Tamanho: {len(response.text)} chars")
            
            # Verificar se tem referências a ASUS/ROG
            if "asus" in response.text.lower():
                print("🎯 Encontradas referências a ASUS na busca DF")
            if "rog" in response.text.lower():
                print("🎯 Encontradas referências a ROG na busca DF")
            if "zephyrus" in response.text.lower():
                print("🎯 Encontradas referências a Zephyrus na busca DF")
        else:
            print(f"❌ Erro na busca DF: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na busca DF: {e}")

if __name__ == "__main__":
    print("🧪 === TESTE DO ANÚNCIO ESPECÍFICO DO DF ===")
    print(f"⏰ {datetime.now()}")
    print()
    
    testar_anuncio_especifico()
    testar_busca_df()
    
    print("\n💡 SOLUÇÕES:")
    print("1. Adicionar busca em regiões específicas (df.olx.com.br)")
    print("2. Melhorar termos de busca")
    print("3. Adicionar busca por URLs específicas")
    print("4. Implementar monitoramento por região") 