# 📚 Componentes da Aplicação - Guia Completo

## 📍 Componentes Comuns (`src/components/common/`)

### Navbar.jsx
**Descrição**: Barra de navegação responsiva com menu desktop e drawer mobile

**Props**: Nenhuma

**Features**:
- Menu desktop com botões
- Drawer lateral para mobile
- Avatar do usuário
- Menu dropdown com logout
- Highlight da página ativa
- Gradiente de cores

**Uso**:
```jsx
import { Navbar } from '@/components/common/Navbar'

<Navbar />
```

---

## 🔐 Formulários (`src/components/forms/`)

### LoginForm.jsx
**Descrição**: Formulário de login com validação

**Props**: Nenhuma

**Features**:
- Validação de usuário/senha
- Campo de senha com toggle visibilidade
- Dados de teste exibidos
- Loading state durante requisição
- Mensagens de erro
- Design atrativo

**Uso**:
```jsx
import { LoginForm } from '@/components/forms/LoginForm'

<LoginForm />
```

---

## 🎨 Componentes de UI (`src/components/ui/`)

### LoadingSpinner.jsx
**Descrição**: Spinner de carregamento com mensagem

**Props**:
- `message` (string): Mensagem exibida (padrão: "Carregando...")

**Uso**:
```jsx
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

<LoadingSpinner message="Carregando funcionários..." />
```

---

### EmptyState.jsx
**Descrição**: Estado vazio quando não há dados

**Props**:
- `title` (string): Título (padrão: "Nenhum item encontrado")
- `message` (string): Mensagem (padrão: "Não há dados para exibir")
- `onAction` (function): Callback do botão
- `actionLabel` (string): Texto do botão (padrão: "Adicionar")

**Uso**:
```jsx
import { EmptyState } from '@/components/ui/EmptyState'

<EmptyState 
  title="Nenhum cliente encontrado" 
  message="Adicione seu primeiro cliente"
  onAction={() => handleAddClick()}
  actionLabel="Adicionar Cliente"
/>
```

---

### SnackbarAlert.jsx
**Descrição**: Notificação em tempo real no canto superior

**Props**:
- `open` (boolean): Controla visibilidade
- `message` (string): Mensagem
- `severity` (string): 'success', 'error', 'warning', 'info'
- `title` (string): Título opcional
- `onClose` (function): Callback ao fechar
- `autoHideDuration` (number): Tempo em ms (padrão: 5000)

**Uso**:
```jsx
import { SnackbarAlert } from '@/components/ui/SnackbarAlert'

<SnackbarAlert 
  open={snackbar.open}
  message="Operação realizada com sucesso!"
  severity="success"
  onClose={snackbar.closeSnackbar}
/>
```

---

### ConfirmDialog.jsx
**Descrição**: Modal de confirmação antes de ações destrutivas

**Props**:
- `open` (boolean): Controla visibilidade
- `title` (string): Título do diálogo
- `message` (string): Mensagem de confirmação
- `onConfirm` (function): Callback ao confirmar
- `onCancel` (function): Callback ao cancelar
- `confirmText` (string): Texto do botão confirmar
- `cancelText` (string): Texto do botão cancelar
- `severity` (string): 'warning' ou 'error'

**Uso**:
```jsx
import { ConfirmDialog } from '@/components/ui/ConfirmDialog'

<ConfirmDialog 
  open={confirmDialog.open}
  title="Confirmar Exclusão"
  message="Tem certeza que deseja deletar?"
  onConfirm={() => handleDelete(id)}
  onCancel={() => setConfirmDialog({ open: false })}
  confirmText="Deletar"
  severity="error"
/>
```

---

### SkeletonLoader.jsx
**Descrição**: Skeleton loading para tabelas

**Props**:
- `count` (number): Quantidade de linhas (padrão: 3)

**Uso**:
```jsx
import { SkeletonLoader } from '@/components/ui/SkeletonLoader'

<SkeletonLoader count={5} />
```

---

### SkeletonCard.jsx
**Descrição**: Skeleton loading para cards em grid

**Props**:
- `count` (number): Quantidade de cards (padrão: 4)

**Uso**:
```jsx
import { SkeletonCard } from '@/components/ui/SkeletonCard'

<SkeletonCard count={4} />
```

---

### StatCard.jsx
**Descrição**: Card de estatística com ícone e trend

**Props**:
- `title` (string): Título do card
- `value` (string|number): Valor exibido
- `icon` (component): Ícone Material UI
- `color` (string): Cor principal (padrão: 'primary')
- `trend` (string): Texto do trend
- `trendDirection` (string): 'up' ou 'down'

**Uso**:
```jsx
import { StatCard } from '@/components/ui/StatCard'
import { People as PeopleIcon } from '@mui/icons-material'

<StatCard 
  title="Total de Clientes" 
  value={47}
  icon={PeopleIcon}
  color="#4caf50"
  trend="+5 este mês"
  trendDirection="up"
/>
```

---

## 📄 Páginas (`src/pages/`)

### Home.jsx
**Descrição**: Dashboard com estatísticas e atalhos

**Features**:
- Grid de 5 stat cards
- Seção de atalhos rápidos
- Cards interativos
- Dados simulados

---

### FuncionariosPage.jsx
**Descrição**: CRUD completo de funcionários

**Features**:
- Tabela com listagem
- Busca por nome/email/CPF
- Adicionar novo
- Editar existente
- Deletar com confirmação
- Validações

---

### ClientesPage.jsx
**Descrição**: CRUD completo de clientes

**Features**:
- Tabela com listagem
- Busca por nome/email/CPF
- Formulário com 7 campos
- CRUD completo
- Validações avançadas

---

### ProdutosPage.jsx
**Descrição**: CRUD de produtos com estoque

**Features**:
- Tabela com estoque visual
- Chips para categoria
- Preço formatado
- Indicador de estoque
- CRUD completo

---

### ComandasPage.jsx
**Descrição**: CRUD de comandas com status

**Features**:
- Tabela com status colorido
- Botão de impressão
- Status: aberta, fechada, paga, cancelada
- Número sequencial
- CRUD completo

---

### CaixaPage.jsx
**Descrição**: Relatório de caixa e movimentações

**Features**:
- 4 cards com resumo financeiro
- Tabela de movimentações
- Adicionar receita/despesa
- Cálculo de lucro líquido
- Categorias e datas

---

## 🎣 Hooks (`src/hooks/`)

### useAuth()
**Descrição**: Hook para acessar contexto de autenticação

**Retorna**:
```js
{
  user,              // Objeto do usuário logado
  loading,           // Estado de carregamento
  error,             // Mensagem de erro
  login,             // Função de login
  logout,            // Função de logout
  isAuthenticated    // Função que retorna boolean
}
```

**Uso**:
```jsx
const { user, login, logout } = useAuth()
```

---

### useValidationRules()
**Descrição**: Hook com regras de validação centralizadas

**Retorna**:
```js
{
  getRule(field),    // Retorna regras para um campo
  getAllRules()      // Retorna todas as regras
}
```

**Regras Disponíveis**:
- nome
- cpf
- email
- senha
- matricula
- valor
- descricao
- categoria
- status
- telefone
- endereco
- cidade
- estado

**Uso**:
```jsx
const { getRule } = useValidationRules()

<Controller
  name="email"
  control={control}
  rules={getRule('email')}
  render={({ field }) => <TextField {...field} />}
/>
```

---

### useLoading()
**Descrição**: Hook para gerenciar estado de loading

**Retorna**:
```js
{
  isLoading,         // boolean
  startLoading,      // () => void
  stopLoading        // () => void
}
```

**Uso**:
```jsx
const { isLoading, startLoading, stopLoading } = useLoading()
```

---

### useSnackbar()
**Descrição**: Hook para gerenciar snackbar

**Retorna**:
```js
{
  open,              // boolean
  message,           // string
  severity,          // string
  showSnackbar,      // (msg, type) => void
  closeSnackbar      // () => void
}
```

**Uso**:
```jsx
const snackbar = useSnackbar()

snackbar.showSnackbar('Sucesso!', 'success')
```

---

## 🔌 Serviços (`src/services/`)

### api.js
**Descrição**: Configuração base do axios

**Features**:
- Base URL configurável
- Interceptor de request
- Interceptor de response
- Tratamento de 401

---

### funcionariosService.js
**Métodos**:
- `getAll()` - Lista todos
- `getById(id)` - Busca por ID
- `create(data)` - Cria novo
- `update(id, data)` - Atualiza
- `delete(id)` - Deleta

---

### clientesService.js
**Métodos**: (Mesmo padrão que funcionariosService)

---

### produtosService.js
**Métodos**: (Mesmo padrão que funcionariosService)

---

### comandasService.js
**Métodos**: (Mesmo padrão que funcionariosService)

---

## 🔄 Context (`src/context/`)

### AuthContext.jsx
**Fornece**:
- `user` - Dados do usuário
- `loading` - Estado de carregamento
- `error` - Erros de autenticação
- `login(username, password)` - Função de login
- `logout()` - Função de logout
- `isAuthenticated()` - Verifica autenticação

**Uso**:
```jsx
<AuthProvider>
  <App />
</AuthProvider>
```

---

## 🛣️ Rotas (`src/routes/`)

### ProtectedRoute.jsx
**Descrição**: Wrapper para rotas protegidas

**Verifica**:
- Se usuário está autenticado
- Redireciona para /login se não

**Uso**:
```jsx
<ProtectedRoute>
  <Home />
</ProtectedRoute>
```

---

### index.jsx
**Descrição**: Configuração de todas as rotas

**Rotas**:
- `/login` - Pública
- `/home` - Protegida (Dashboard)
- `/funcionarios` - Protegida
- `/clientes` - Protegida
- `/produtos` - Protegida
- `/comandas` - Protegida
- `/caixa` - Protegida

---

## 🎨 Tema (`src/theme.js`)

**Configurações**:
- Paleta de cores
- Tipografia customizada
- Componentes customizados
- Breakpoints responsivos
- Sombras e elevações

---

## 💾 State Management

### Context API
- Autenticação global em `AuthContext`
- Dados do usuário em `sessionStorage`

### Local State
- Cada página gerencia seu próprio estado
- Componentes controlados com `useState`

---

## 📊 Estrutura de Dados

### Usuário
```js
{
  username: string,
  email: string,
  role: string,
  loginTime: string (ISO)
}
```

### Funcionário
```js
{
  id: number,
  nome: string,
  cpf: string,
  email: string,
  matricula: string,
  senha: string
}
```

### Cliente
```js
{
  id: number,
  nome: string,
  cpf: string,
  email: string,
  telefone: string,
  endereco: string,
  cidade: string,
  estado: string
}
```

### Produto
```js
{
  id: number,
  nome: string,
  descricao: string,
  preco: number,
  categoria: string,
  estoque: number
}
```

### Comanda
```js
{
  id: number,
  numero: number,
  cliente: string,
  descricao: string,
  valor: number,
  status: 'aberta' | 'fechada' | 'paga' | 'cancelada'
}
```

---

## ✨ Boas Práticas

1. **Componentes**: Sempre funcionais e reutilizáveis
2. **Props**: Bem tipadas com JSDoc
3. **Hooks**: Reutilização de lógica comum
4. **Context**: Apenas para estado global
5. **Services**: Chamadas de API centralizadas
6. **Validação**: Regras centralizadas
7. **Feedback**: Sempre informar usuário
8. **Responsividade**: Mobile-first
9. **Performance**: Minimizar re-renders
10. **Acessibilidade**: Labels e ARIA

---

**Versão**: 1.0.0
**Última atualização**: Maio 2026
