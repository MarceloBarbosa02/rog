#!/usr/bin/env python3
# monitor_simples.py - Teste simples de monitoramento

import requests
import re
from datetime import datetime
import time

def testar_mercadolivre():
    """Teste básico no Mercado Livre"""
    print("🔍 Testando busca no Mercado Livre...")
    
    url = "https://api.mercadolibre.com/sites/MLB/search"
    params = {
        'q': 'ASUS ROG Zephyrus M16',
        'category': 'MLB1649',  # Notebooks
        'limit': 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            resultados = dados.get('results', [])
            
            print(f"✅ Mercado Livre conectado! Encontrados {len(resultados)} resultados")
            
            for i, item in enumerate(resultados, 1):
                titulo = item.get('title', '')
                preco = item.get('price', 0)
                
                # Verificar características importantes
                score = 0
                caracteristicas = []
                
                titulo_lower = titulo.lower()
                if "anime matrix" in titulo_lower:
                    score += 15
                    caracteristicas.append("🎯 AniMe Matrix")
                if "gu604" in titulo_lower:
                    score += 15
                    caracteristicas.append("🎯 GU604")
                if "mini led" in titulo_lower:
                    score += 12
                    caracteristicas.append("🎯 Mini LED")
                if "240hz" in titulo_lower:
                    score += 8
                    caracteristicas.append("⭐ 240Hz")
                if "zephyrus m16" in titulo_lower:
                    score += 12
                    caracteristicas.append("🎯 Zephyrus M16")
                if "asus" in titulo_lower and "rog" in titulo_lower:
                    score += 8
                    caracteristicas.append("✓ ASUS ROG")
                
                # Análise de preço
                suspeita = ""
                if preco < 3000:
                    suspeita = "🚨 EXTREMAMENTE SUSPEITO"
                elif preco < 5000:
                    suspeita = "⚠️ MUITO SUSPEITO"
                elif preco < 8000:
                    suspeita = "⚠️ SUSPEITO"
                else:
                    suspeita = "💰 PREÇO NORMAL"
                
                print(f"\n{i}. Score: {score} | {suspeita}")
                print(f"   📝 {titulo[:60]}...")
                print(f"   💰 R$ {preco:,}")
                if caracteristicas:
                    print(f"   ✅ {', '.join(caracteristicas)}")
                
        else:
            print(f"❌ Erro HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

def testar_olx():
    """Teste básico na OLX"""
    print("\n🔍 Testando acesso à OLX...")
    
    url = "https://www.olx.com.br/informatica/notebooks-netbooks"
    params = {'q': 'ASUS ROG Zephyrus M16'}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            print(f"✅ OLX conectado! Resposta de {len(response.text)} caracteres")
            
            # Buscar por padrões básicos no HTML
            if "asus" in response.text.lower():
                print("🎯 Encontradas referências a ASUS na página")
            if "rog" in response.text.lower():
                print("🎯 Encontradas referências a ROG na página")
                
        else:
            print(f"❌ OLX erro HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro OLX: {e}")

def main():
    print("🚀 === TESTE SIMPLES DE MONITORAMENTO ===")
    print(f"⏰ {datetime.now()}")
    print()
    
    # Testar conectividade básica
    print("🌐 Testando conectividade...")
    try:
        response = requests.get("https://httpbin.org/ip", timeout=5)
        if response.status_code == 200:
            print("✅ Internet funcionando")
        else:
            print("❌ Problema de conectividade")
            return
    except:
        print("❌ Sem conexão com internet")
        return
    
    print()
    
    # Testar sites principais
    testar_mercadolivre()
    time.sleep(2)
    testar_olx()
    
    print()
    print("🎉 Teste concluído!")
    print()
    print("💡 Se este teste funcionou, seus scripts principais também devem funcionar.")
    print("🔧 Se não funcionou, verifique:")
    print("   - Conexão com internet")
    print("   - Instalação do Python requests: pip install requests")
    print("   - Firewall ou proxy bloqueando")

if __name__ == "__main__":
    main() 