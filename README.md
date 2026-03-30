# Projeto Rio Amazonas - Dashboard

Interface web moderna para monitoramento de dados fluviométricos do Rio Amazonas.

## 🚀 Como executar

### Opção 1: Dashboard HTML (Recomendado - Sem dependências)

1. Execute apenas o backend:
```bash
python -m uvicorn backend.api:app --host 0.0.0.0 --port 5000 --reload
```

2. Abra o dashboard:
   - Abra `frontend/public/dashboard.html` no navegador diretamente
   - OU use um servidor local: `python -m http.server 8000` e acesse `http://localhost:8000/frontend/public/dashboard.html`

### Opção 2: React (Requer Node.js)

1. Backend:
```bash
python -m uvicorn backend.api:app --host 0.0.0.0 --port 5000 --reload
```

2. Frontend:
```bash
cd frontend
npm install
npm run dev
```
Acesse: `http://localhost:5173`

## 📊 Funcionalidades

- **Dashboard interativo** com dados de múltiplas estações
- **Gráficos de vazão e cota** usando Chart.js
- **Tabelas de dados** com formatação de datas
- **Atualização em tempo real** dos dados
- **Fallback automático** quando API não responde
- **Múltiplas estações**: Manaus, Itacoatiara, Parintins, Óbidos, Tefé
- **Gráfico mensal de tendência** de cota para comparativo histórico
- **Interface responsiva** para desktop e mobile

## 🏗️ Arquitetura

- **Backend**: FastAPI servindo dados JSON
- **Frontend**: HTML/CSS/JS puro com Chart.js (ou React opcional)
- **Dados**: Integração com Open-Meteo API + fallback local
- **Estilos**: CSS moderno com design responsivo

## 📁 Estrutura do projeto

```
projeto-rio-amazonas/
├── pyproject.toml         # Configuração do projeto Python
├── requirements.txt       # Dependências Python
├── README.md              # Este arquivo
├── backend/               # Backend Python
│   ├── api.py            # Servidor FastAPI
│   ├── src/              # Código Python principal
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api.py        # Módulo de busca de dados
│   │   ├── processamento.py
│   │   └── utils.py
│   └── data/
│       └── fallback.json # Dados de fallback
└── frontend/             # Frontend React
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── public/           # Arquivos estáticos
    │   ├── dashboard.html
    │   └── teste.html
    └── src/
        ├── App.jsx
        ├── App.css
        └── main.jsx
```

## 🔧 Desenvolvimento

### Executando testes

```bash
# Backend
python backend/src/main.py

# Dashboard HTML
python -m http.server 8000
# Acesse: http://localhost:8000/frontend/public/dashboard.html
```

### API Endpoints

- `GET /api/dados` - Retorna dados de todas as estações
- `GET /api/estacoes` - Lista todas as estações disponíveis
