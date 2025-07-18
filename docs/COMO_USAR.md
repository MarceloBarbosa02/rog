# 📖 Como Usar o Monitor ASUS ROG

## 🚀 Execução Rápida

### Teste Simples
```bash
cd ~/monitor_asus_rog/scripts
python3 monitor_asus_rog.py
```

### Monitoramento Completo
```bash
cd ~/monitor_asus_rog/scripts
python3 monitor_completo.py
```

### Execução Contínua
```bash
cd ~/monitor_asus_rog/scripts
./monitor_continuo.sh &
```

## 📊 Verificar Resultados

### Últimos Resultados
```bash
# Ver últimos candidatos
ls -la ~/monitor_asus_rog/resultados/ | tail -5

# Ver conteúdo do último arquivo
cat ~/monitor_asus_rog/resultados/candidatos_*.json | jq '.'
```

### Análise Avançada
```bash
cd ~/monitor_asus_rog/scripts
python3 analise_avancada.py
```

### Verificar Logs
```bash
# Ver logs em tempo real
tail -f ~/monitor_asus_rog/logs/monitor.log

# Ver últimas 50 linhas
tail -n 50 ~/monitor_asus_rog/logs/monitor.log
```

## 🚨 Sistema de Alertas

### Níveis de Alerta
- **🚨 ALERTA MÁXIMO** (Score 40+): Verificar IMEDIATAMENTE
- **⚠️ ALERTA ALTO** (Score 30+): Alta prioridade
- **⚠️ ALERTA MÉDIO** (Score 20+): Monitorar de perto
- **ℹ️ MONITORAR** (Score 10+): Acompanhar

### Verificar Alertas
```bash
ls ~/monitor_asus_rog/alertas/
cat ~/monitor_asus_rog/alertas/alerta_*.txt
```

## ⚙️ Configurações

### Editar Configurações
```bash
nano ~/monitor_asus_rog/config/config.json
```

### Alterar Intervalo de Monitoramento
Edite `intervalo_horas` no arquivo config.json

### Configurar E-mail de Alertas
Edite `email_notificacoes` no arquivo config.json

## 🔍 Sites Monitorados

### Automáticos
- ✅ **Mercado Livre**: Via API oficial
- ✅ **OLX**: Via web scraping

### Manuais (Requer verificação manual)
- 📱 **Facebook Marketplace**: Usar app/site
- 🛍️ **Enjoei**: Verificação manual
- 🔄 **Outros**: Conforme necessário

## 📱 Comandos Úteis

### Parar Monitoramento
```bash
pkill -f monitor_continuo.sh
```

### Limpar Logs Antigos
```bash
find ~/monitor_asus_rog/logs -name "*.log" -mtime +7 -delete
```

### Backup dos Resultados
```bash
tar -czf backup_resultados_$(date +%Y%m%d).tar.gz ~/monitor_asus_rog/resultados/
```

## 🆘 Troubleshooting

### Erro de Dependências
```bash
pip3 install --user requests beautifulsoup4 lxml
```

### Erro de Permissões
```bash
chmod +x ~/monitor_asus_rog/scripts/*.sh
chmod +x ~/monitor_asus_rog/scripts/*.py
```

### Limpar Cache
```bash
rm -rf ~/monitor_asus_rog/resultados/*
rm -rf ~/monitor_asus_rog/logs/*
```
```

---

## **🎯 Resumo dos Scripts Criados:**

1. **README.md** - Documentação principal
2. **setup.sh** - Configuração inicial
3. **monitor_asus_rog.py** - Monitoramento Mercado Livre
4. **monitor_continuo.sh** - Execução contínua
5. **verificar_resultados.py** - Análise básica
6. **monitor_olx.py** - Monitoramento OLX especializado
7. **monitor_facebook.py** - Guia Facebook Marketplace
8. **monitor_completo.py** - Execução de todos os monitoramentos
9. **analise_avancada.py** - Análise de tendências e padrões
10. **config.json** - Configurações completas
11. **COMO_USAR.md** - Guia de uso detalhado

**Agora você tem um sistema COMPLETO de monitoramento!** 🚀

**Copie todos esses códigos para seus respectivos arquivos e você terá um sistema profissional de recuperação de notebook!**