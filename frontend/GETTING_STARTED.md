# 🚀 Guia de Início Rápido - Comandas do Zé

## ⚙️ Requisitos do Sistema

- **Node.js** 16.x ou superior
- **npm** 8.x ou superior (incluído no Node.js)
- **Git** (opcional, para controle de versão)

## 📥 Instalação

### 1. Clonar/Baixar o Projeto

```bash
cd c:\Users\seu_usuario\Desktop\faculdade\comandas_api\frontend
```

### 2. Instalar Dependências

**Opção 1: Windows (Executar script)**
```bash
setup.bat
```

**Opção 2: Terminal (Windows/Mac/Linux)**
```bash
npm install
```

**Opção 3: Usar Yarn**
```bash
yarn install
```

## ▶️ Executar a Aplicação

### Desenvolvimento

```bash
npm run dev
```

A aplicação abrirá automaticamente em: http://localhost:3000

### Build para Produção

```bash
npm run build
```

Gera arquivos otimizados em `dist/`

### Preview do Build

```bash
npm run preview
```

## 🔑 Credenciais de Teste

Ao acessar a página de login, use:

| Campo | Valor |
|-------|-------|
| Usuário | `abc` |
| Senha | `bolinhas` |

## 🎯 Navegação

Após fazer login, você terá acesso a:

1. **Dashboard (Home)**
   - Estatísticas gerais
   - Atalhos rápidos
   - Resumo do negócio

2. **Funcionários**
   - Listar funcionários
   - Adicionar novo
   - Editar existentes
   - Deletar funcionários

3. **Clientes**
   - Gerenciar clientes
   - Informações completas
   - Contato e endereço

4. **Produtos**
   - Catálogo de produtos
   - Preços e categorias
   - Controle de estoque

5. **Comandas**
   - Criar comandas
   - Rastrear status
   - Imprimir comandas

6. **Caixa**
   - Relatório de receitas/despesas
   - Movimentações
   - Saldo atual

## 📱 Responsividade

A aplicação funciona perfeitamente em:
- ✅ Desktop (1920px+)
- ✅ Laptop (1280px+)
- ✅ Tablet (960px+)
- ✅ Smartphone (600px+)

**Teste em seu dispositivo!**

## 🎨 Interface

### Temas de Cores por Seção

| Seção | Cor | Gradiente |
|-------|-----|----------|
| Funcionários | Azul | #1976d2 → #1565c0 |
| Clientes | Verde | #4caf50 → #45a049 |
| Produtos | Laranja | #ff9800 → #f57c00 |
| Comandas | Roxo | #9c27b0 → #7b1fa2 |
| Caixa | Vermelho | #f44336 → #d32f2f |

## 📊 Funcionalidades Principais

### CRUD Completo (Create, Read, Update, Delete)

Todas as páginas de gerenciamento possuem:

- ✅ **Tabelas** com listagem de dados
- ✅ **Busca** para filtrar dados
- ✅ **Formulários** para adicionar/editar
- ✅ **Diálogos** com confirmação de exclusão
- ✅ **Validações** em tempo real
- ✅ **Feedback visual** com notificações
- ✅ **Loading states** durante operações
- ✅ **Empty states** quando sem dados

### Autenticação

- ✅ Login com usuário e senha
- ✅ Persistência em sessionStorage
- ✅ Logout com limpeza de sessão
- ✅ Redirecionamento automático
- ✅ Proteção de rotas

### UX/UI Moderna

- ✅ Navbar responsiva
- ✅ Drawer para mobile
- ✅ Animações suaves
- ✅ Transições elegantes
- ✅ Ícones Material Design
- ✅ Cards com hover effects
- ✅ Botões com feedback tátil

## ⚙️ Configuração da API

A aplicação conecta com a API em:

```
https://127.0.0.1:8443
```

Se precisar mudar, edite:

```
frontend/.env
```

Ou modifique em `src/services/api.js`:

```js
const API_BASE_URL = 'https://seu-api.com'
```

## 🐛 Solução de Problemas

### npm não está instalado

**Solução**: Instale Node.js de https://nodejs.org/

### Porta 3000 já está em uso

**Solução**: Mude a porta em `vite.config.js`:

```js
server: {
  port: 3001,  // Mude para outra porta
  open: true
}
```

### Não consegue conectar na API

**Solução**: 
- Verifique se a API está rodando
- Verifique o certificado SSL
- Verifique o CORS da API

### Erro de validação nos formulários

**Solução**: 
- Verifique os dados inseridos
- Consulte as regras em `src/hooks/useValidationRules.js`

## 📝 Estrutura de Pastas

```
frontend/
├── public/          # Assets estáticos
├── src/
│   ├── components/  # Componentes React
│   ├── context/     # Context API
│   ├── hooks/       # Hooks customizados
│   ├── pages/       # Páginas da aplicação
│   ├── routes/      # Configuração de rotas
│   ├── services/    # Serviços de API
│   ├── styles/      # CSS global
│   ├── App.jsx      # Componente raiz
│   └── main.jsx     # Ponto de entrada
├── package.json     # Dependências
├── vite.config.js   # Configuração Vite
└── index.html       # HTML template
```

## 🔄 Fluxo de Autenticação

```
1. Acessa /login
   ↓
2. Preenche formulário (abc / bolinhas)
   ↓
3. Valida credenciais (mockado)
   ↓
4. Salva em sessionStorage
   ↓
5. Redireciona para /home
   ↓
6. Acessa rotas protegidas
   ↓
7. Clica Logout
   ↓
8. Limpa sessionStorage
   ↓
9. Redireciona para /login
```

## 💡 Dicas

1. **Limpar Cache do Navegador**: Pressione Ctrl+Shift+Delete
2. **DevTools React**: Instale extensão no Chrome/Firefox
3. **Console do Navegador**: Pressione F12
4. **Modo Responsivo**: Pressione F12 → Toggle device toolbar

## 📚 Documentação Completa

Para documentação mais detalhada, consulte:

- [README.md](README.md) - Visão geral
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura e padrões
- [ENV.md](ENV.md) - Variáveis de ambiente

## 🎓 Aprendizados Principais

Esta aplicação demonstra:

- React 18 com Hooks
- React Router v6
- Material UI 5
- React Hook Form com validações
- Context API
- Axios para chamadas HTTP
- CSS-in-JS com Emotion
- Vite como bundler
- Componentes funcionais reutilizáveis
- Boas práticas de React 2026

## 📞 Suporte

Em caso de dúvidas, verifique:

1. Se o Node.js está instalado: `node --version`
2. Se as dependências foram instaladas: `npm list`
3. Se a aplicação está rodando: Abra http://localhost:3000
4. Console do navegador para erros (F12)

## 🎉 Próximas Etapas

Depois de configurar, você pode:

1. Modificar cores em `src/theme.js`
2. Adicionar novos componentes em `src/components/`
3. Criar novas páginas em `src/pages/`
4. Estender funcionalidades nos serviços
5. Adicionar testes automatizados

---

**Bem-vindo ao Comandas do Zé! 🍺**

Versão: 1.0.0
Desenvolvido com ❤️
