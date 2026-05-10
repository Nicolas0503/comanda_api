# Comandas do Zé - Frontend

Aplicação web completa para gerenciamento de comandas usando React + Vite.

## 🚀 Iniciar a Aplicação

### Pré-requisitos
- Node.js 16+ instalado
- npm ou yarn

### Instalação

1. Entre no diretório do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Inicie o servidor de desenvolvimento:
```bash
npm run dev
```

A aplicação abrirá automaticamente em `http://localhost:3000`

## 📋 Dados de Teste

**Usuário:** abc
**Senha:** bolinhas

## 🏗️ Estrutura do Projeto

```
src/
├── components/
│   ├── common/          # Navbar, Layout
│   ├── forms/           # LoginForm
│   └── ui/              # Cards, Tables, Loading, Dialogs
├── context/             # AuthContext
├── hooks/               # useAuth, useValidationRules, useSnackbar
├── pages/               # Home, CRUDs
├── services/            # API integration
├── routes/              # Router setup
├── styles/              # CSS files
├── theme.js             # MUI theme customizado
├── App.jsx              # Root component
└── main.jsx             # Entry point
```

## 🎨 Tecnologias

- React 18.2.0
- Vite 5.0.0
- React Router DOM 6.20
- Material UI 5.14
- React Hook Form 7.48
- Axios 1.6
- Emotion (CSS-in-JS)

## 📱 Responsividade

A aplicação é totalmente responsiva com breakpoints:
- xs: 0px
- sm: 600px
- md: 960px
- lg: 1280px

## 🔐 Autenticação

- Sistema baseado em sessionStorage
- Usuário/senha mockados
- Redirect automático para login
- Logout com limpeza de sessão

## 📦 Build

```bash
npm run build
```

Gera arquivos otimizados em `dist/`

## 🐛 Desenvolvimento

Todos os componentes seguem:
- Hooks Pattern
- Context API
- Clean Code
- Componentização
- Separação de responsabilidades

## 📄 Funcionalidades

- ✅ Autenticação com sessionStorage
- ✅ Dashboard com estatísticas
- ✅ CRUD Funcionários
- ✅ CRUD Clientes
- ✅ CRUD Produtos
- ✅ CRUD Comandas
- ✅ Relatório de Caixa
- ✅ Navbar responsiva
- ✅ Validações com React Hook Form
- ✅ Feedback visual com Snackbar
- ✅ Integração com API REST

## 🔗 API

A aplicação conecta a uma API REST rodando em:
`https://127.0.0.1:8443`

Endpoints:
- `/funcionarios`
- `/clientes`
- `/produtos`
- `/comandas`

## 📝 Notas

- Os dados são persistidos via sessionStorage para autenticação
- As chamadas à API são feitas via axios
- Material UI fornece componentes prontos
- Theme customizado aplica estilo uniforme

---

Desenvolvido com ❤️ para Comandas do Zé
