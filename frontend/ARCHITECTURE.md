# 📋 Guia de Arquitetura - Comandas do Zé

## 🏗️ Estrutura de Diretórios

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Navbar.jsx          # Barra de navegação responsiva
│   │   │   └── index.js
│   │   ├── forms/
│   │   │   ├── LoginForm.jsx       # Formulário de login
│   │   │   ├── LoginForm.css
│   │   │   └── index.js
│   │   └── ui/
│   │       ├── LoadingSpinner.jsx
│   │       ├── EmptyState.jsx
│   │       ├── SnackbarAlert.jsx
│   │       ├── ConfirmDialog.jsx
│   │       ├── SkeletonLoader.jsx
│   │       ├── SkeletonCard.jsx
│   │       ├── StatCard.jsx
│   │       └── index.js
│   ├── context/
│   │   └── AuthContext.jsx         # Context de autenticação
│   ├── hooks/
│   │   ├── useAuth.js              # Hook de autenticação
│   │   ├── useValidationRules.js   # Hook com regras de validação
│   │   ├── useLoading.js           # Hook para gerenciar loading
│   │   └── useSnackbar.js          # Hook para snackbar
│   ├── pages/
│   │   ├── Home.jsx                # Dashboard
│   │   ├── FuncionariosPage.jsx    # CRUD Funcionários
│   │   ├── ClientesPage.jsx        # CRUD Clientes
│   │   ├── ProdutosPage.jsx        # CRUD Produtos
│   │   ├── ComandasPage.jsx        # CRUD Comandas
│   │   └── CaixaPage.jsx           # Relatório de Caixa
│   ├── routes/
│   │   ├── index.jsx               # Configuração de rotas
│   │   └── ProtectedRoute.jsx      # Componente para rotas protegidas
│   ├── services/
│   │   ├── api.js                  # Configuração do axios
│   │   ├── funcionariosService.js  # Service para funcionários
│   │   ├── clientesService.js      # Service para clientes
│   │   ├── produtosService.js      # Service para produtos
│   │   └── comandasService.js      # Service para comandas
│   ├── styles/
│   │   └── (arquivos CSS globais)
│   ├── App.jsx                     # Componente raiz
│   ├── main.jsx                    # Ponto de entrada
│   ├── index.css                   # Estilos globais
│   └── theme.js                    # Tema Material UI
├── index.html                      # HTML template
├── package.json                    # Dependências e scripts
├── vite.config.js                  # Configuração do Vite
├── .env.example                    # Exemplo de variáveis de ambiente
├── README.md                       # Documentação principal
└── ARCHITECTURE.md                 # Este arquivo
```

## 🎯 Padrões de Arquitetura

### 1. **Context API para Estado Global**
- `AuthContext` gerencia autenticação globalmente
- `sessionStorage` persiste dados do usuário
- Redirecionamento automático em caso de sessão expirada

### 2. **Hooks Customizados**
- `useAuth()` - Acesso ao contexto de autenticação
- `useValidationRules()` - Regras de validação centralizadas
- `useLoading()` - Gerenciamento de estado de carregamento
- `useSnackbar()` - Feedback visual para o usuário

### 3. **React Hook Form**
- Validação de formulários
- Redução de re-renders
- Integração com Controller para componentes MUI

### 4. **Separação de Responsabilidades**
- **Components**: Apenas apresentação (UI)
- **Services**: Chamadas à API
- **Hooks**: Lógica reutilizável
- **Context**: Estado global
- **Pages**: Páginas completas

### 5. **Material UI + Emotion**
- Sistema de design consistente
- Temas customizáveis
- Responsividade built-in
- Componentes prontos e acessíveis

## 🔄 Fluxo de Dados

```
User Input → Component → Hook/Service → Context/State → Component Update
     ↓           ↓              ↓              ↓              ↓
  UI Events   FormData    API Call      Auth State      UI Rendered
```

## 🔐 Autenticação

### Fluxo:
1. Usuário acessa `/login`
2. Submete credenciais (mockadas: abc / bolinhas)
3. `AuthContext.login()` verifica credenciais
4. Se válido, persiste em `sessionStorage`
5. Redireciona para `/home`
6. `ProtectedRoute` valida autenticação para rotas protegidas
7. Logout limpa sessionStorage e redireciona para `/login`

## 📱 Responsividade

### Breakpoints MUI:
- `xs`: 0px - Mobile
- `sm`: 600px - Tablet pequeno
- `md`: 960px - Tablet
- `lg`: 1280px - Desktop
- `xl`: 1920px - Desktop grande

### Implementação:
```jsx
<Box sx={{
  display: 'grid',
  gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: '1fr 1fr 1fr 1fr' },
  gap: 2
}} />
```

## 🎨 Tema Customizado

### Cores Primárias:
- `primary`: #1976d2 (Azul)
- `secondary`: #dc004e (Rosa)
- `success`: #4caf50 (Verde)
- `warning`: #ff9800 (Laranja)
- `error`: #f44336 (Vermelho)
- `info`: #2196f3 (Azul claro)

### Componentes Customizados:
- `MuiButton`: Sombra e hover com transform
- `MuiCard`: Sombra elevada no hover
- `MuiTextField`: Borda com focus animado
- `MuiAppBar`: Gradiente personalizado

## 📊 CRUD Pattern

Cada página CRUD segue o padrão:

```jsx
const [data, setData] = useState([])
const [loading, setLoading] = useState(false)
const [openDialog, setOpenDialog] = useState(false)

// Fetch
const fetch = async () => { /* ... */ }

// Open/Close Dialog
const handleOpenDialog = (item) => { /* ... */ }

// Submit
const onSubmit = async (data) => { /* ... */ }

// Delete
const handleDelete = async (id) => { /* ... */ }

// Render
return (
  <Table> {/* Listagem */}
  <Dialog> {/* Formulário */}
  <ConfirmDialog> {/* Confirmação */}
  <SnackbarAlert> {/* Feedback */}
)
```

## 🛠️ Serviços de API

Cada serviço segue o padrão CRUD:

```js
export const service = {
  async getAll() { /* GET */ }
  async getById(id) { /* GET byId */ }
  async create(data) { /* POST */ }
  async update(id, data) { /* PUT */ }
  async delete(id) { /* DELETE */ }
}
```

Retorno padronizado:
```js
{ success: true, data: [...] }
{ success: false, error: 'mensagem' }
```

## ✅ Validações

Centralizadas em `useValidationRules()`:

```js
const rules = {
  nome: {
    required: 'Nome é obrigatório',
    minLength: { value: 3, message: '...' }
  },
  email: {
    required: 'Email é obrigatório',
    pattern: { value: /regex/, message: '...' }
  },
  cpf: { /* ... */ },
  senha: { /* ... */ }
}
```

## 🎯 Boas Práticas Implementadas

✅ Hooks em vez de Class Components
✅ Functional Components
✅ Separation of Concerns
✅ DRY (Don't Repeat Yourself)
✅ Context API para estado global
✅ Session Storage para persistência
✅ Validação de formulários robusta
✅ Tratamento de erros
✅ Loading states
✅ Empty states
✅ Responsividade mobile-first
✅ Acessibilidade (labels, aria-labels)
✅ Código limpo e bem organizado
✅ Componentes reutilizáveis
✅ Tipagem com JSDoc onde necessário

## 🚀 Performance

- Virtual DOM do React
- Code splitting automático do Vite
- Lazy loading de rotas (possível adicionar)
- Memoization de componentes pesados
- Otimização de re-renders com hooks
- CSS-in-JS (Emotion) com tree-shaking

## 📝 Convenções de Nomeação

- **Componentes**: PascalCase (e.g., `LoginForm.jsx`)
- **Hooks**: camelCase com prefixo `use` (e.g., `useAuth.js`)
- **Variáveis/Funções**: camelCase (e.g., `handleSubmit`)
- **Constantes**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)
- **Arquivos CSS**: kebab-case (e.g., `login-form.css`)

## 🔗 Integração com Backend

### Endpoints esperados:
- `GET /funcionarios` - Listar funcionários
- `POST /funcionarios` - Criar funcionário
- `PUT /funcionarios/{id}` - Atualizar funcionário
- `DELETE /funcionarios/{id}` - Deletar funcionário

(Mesmo padrão para clientes, produtos, comandas)

### Headers necessários:
```js
{
  'Content-Type': 'application/json',
  'Authorization': 'Bearer {token}'  // se necessário
}
```

## 🐛 Debugging

### Ferramentas recomendadas:
- React DevTools
- Redux DevTools (se adicionar Redux)
- Network tab do navegador
- Console do navegador

### Verificar autenticação:
```js
sessionStorage.getItem('user')
```

## 📚 Próximas Melhorias

- [ ] Adicionar lazy loading de componentes
- [ ] Implementar erro boundary
- [ ] Adicionar testes unitários (Jest)
- [ ] Adicionar testes E2E (Cypress)
- [ ] Implementar PWA
- [ ] Adicionar analíticos
- [ ] Implementar dark mode
- [ ] Adicionar paginação nas tabelas
- [ ] Adicionar filtros avançados
- [ ] Implementar relatórios em PDF

---

**Versão**: 1.0.0
**Última atualização**: Maio 2026
