# 🔍 Monitor ASUS ROG Zephyrus M16 - Sistema de Recuperação

Sistema automatizado para monitorar e detectar seu notebook ASUS ROG Zephyrus M16 roubado em plataformas de venda online.

## 📋 Características do Notebook Monitorado

- **Modelo**: ASUS ROG Zephyrus M16 (2023)
- **Código**: GU604
- **Tela**: 16" QHD+ (2560x1600) 240Hz Mini LED
- **Tecnologia Única**: AniMe Matrix™ (tampa com LEDs animados)
- **Refrigeração**: ROG Intelligent Cooling
- **Valor Original**: ~R$ 15.000

## 🚀 Instalação Rápida

```bash
# 1. Navegar para o projeto
cd ~/monitor_asus_rog

# 2. Executar configuração
chmod +x setup.sh
./setup.sh

# 3. Fazer teste inicial
cd scripts
python3 monitor_asus_rog.py
```

## 🔍 Como Usar

### Execução Manual
```bash
cd ~/monitor_asus_rog/scripts
python3 monitor_asus_rog.py
```

### Execução Contínua
```bash
cd ~/monitor_asus_rog/scripts
./monitor_continuo.sh &
```

## 🚨 Sistema de Alertas

- **🚨 ALERTA MÁXIMO** (Score 40+): Correspondência muito alta
- **⚠️ ALERTA ALTO** (Score 30+): Correspondência alta  
- **⚠️ ALERTA MÉDIO** (Score 20+): Correspondência moderada

## ⚖️ Considerações Legais

- ✅ Use apenas para recuperar SEU próprio dispositivo
- ✅ Trabalhe com autoridades policiais
- ❌ Não confronte suspeitos diretamente