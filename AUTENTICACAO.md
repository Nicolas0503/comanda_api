# GUIA DE AUTENTICAÇÃO E AUTORIZAÇÃO - API Pastelaria

## Visão Geral
A API agora implementa autenticação JWT com access tokens (15 min) e refresh tokens (7 dias), com controle de acesso por grupo.

---

## FLUXO DE AUTENTICAÇÃO

### 1. LOGIN - Obter Tokens
**POST** `/auth/login`

Exemplo de Request:
```json
{
  "usuario_id": 1,
  "senha": "123456",
  "grupo": 1
}
```

Response (Sucesso - 200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Response (Erro - 401):
```json
{
  "detail": "Credenciais inválidas"
}
```

---

### 2. USAR ACCESS TOKEN - Chamadas Autenticadas
**Adicionar header em qualquer requisição autenticada:**
```
Authorization: Bearer {access_token}
```

Exemplo de requisição:
```bash
curl -H "Authorization: Bearer seu_access_token_aqui" http://localhost:8000/funcionario/
```

---

### 3. REFRESH TOKEN - Renovar Acesso
**POST** `/auth/refresh`

Quando o access token expirar, use o refresh token para gerar novos tokens:
```json
{
  "refresh_token": "seu_refresh_token_aqui"
}
```

Response:
```json
{
  "access_token": "novo_access_token",
  "refresh_token": "novo_refresh_token",
  "token_type": "bearer"
}
```

---

### 4. OBTER INFORMAÇÕES DO USUÁRIO
**GET** `/auth/me`

Header:
```
Authorization: Bearer {access_token}
```

Response (200):
```json
{
  "usuario_id": 1,
  "grupo": 1
}
```

---

### 5. LOGOUT
**POST** `/auth/logout`

Header:
```
Authorization: Bearer {access_token}
```

Response (200):
```json
{
  "detail": "Logout realizado com sucesso"
}
```

---

## PERMISSÕES POR ROTA

### FUNCIONÁRIO
| Rota | Método | Permissão | Descrição |
|------|--------|-----------|-----------|
| `/funcionario/` | GET | Grupo 1 | Listar todos |
| `/funcionario/{id}` | GET | Autenticado | Listar um |
| `/funcionario/` | POST | Grupo 1 | Criar |
| `/funcionario/{id}` | PUT | Grupo 1 | Editar |
| `/funcionario/{id}` | DELETE | Grupo 1 | Excluir |

### CLIENTE
| Rota | Método | Permissão | Descrição |
|------|--------|-----------|-----------|
| `/cliente/` | GET | Autenticado | Listar todos |
| `/cliente/{id}` | GET | Autenticado | Listar um |
| `/cliente/` | POST | Grupos 1, 3 | Criar |
| `/cliente/{id}` | PUT | Grupos 1, 3 | Editar |
| `/cliente/{id}` | DELETE | Grupo 1 | Excluir |

### PRODUTO
| Rota | Método | Permissão | Descrição |
|------|--------|-----------|-----------|
| `/produto/publico` | GET | Pública | Listar todos (sem id e valor) |
| `/produto/` | GET | Autenticado | Listar todos (completo) |
| `/produto/{id}` | GET | Autenticado | Listar um |
| `/produto/` | POST | Grupo 1 | Criar |
| `/produto/{id}` | PUT | Grupo 1 | Editar |
| `/produto/{id}` | DELETE | Grupo 1 | Excluir |

### AUTH
| Rota | Método | Permissão | Descrição |
|------|--------|-----------|-----------|
| `/auth/login` | POST | Pública | Login |
| `/auth/refresh` | POST | Pública | Renovar token |
| `/auth/me` | GET | Autenticado | Informações do usuário |
| `/auth/logout` | POST | Pública | Logout |

### ROOT
| Rota | Método | Permissão | Descrição |
|------|--------|-----------|-----------|
| `/` | GET | Pública | Informação da API |

---

## CÓDIGOS DE ERRO

### 401 - Não Autenticado
Retornado quando:
- Token não fornecido
- Token inválido ou expirado
- Token de tipo errado (ex: usar refresh token em lugar de access token)

```json
{
  "detail": "Token não fornecido | Token inválido | Token expirado"
}
```

### 403 - Acesso Negado
Retornado quando o usuário não tem permissão (grupo diferente):

```json
{
  "detail": "Acesso negado. Grupos permitidos: [1]"
}
```

---

## ESTRUTURA DE GRUPOS

| Grupo | Descrição | Permissões |
|-------|-----------|-----------|
| 1 | Admin | Acesso completo |
| 2 | (Outro) | - |
| 3 | Gerente | Criar/editar clientes |

---

## EXEMPLO PRÁTICO COMPLETO

### Passo 1: Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "senha": "123456",
    "grupo": 1
  }'
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c3VhcmlvX2lkIjogMSwgImdydXBvIjogMSwgInRpcG8iOiAiYWNjZXNzIiwgImlhdCI6IDE2MTYyMzkwMjIsICJleHAiOiAxNjE2MjM5OTIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c3VhcmlvX2lkIjogMSwgImdydXBvIjogMSwgInRpcG8iOiAicmVmcmVzaCIsICJpYXQiOiAxNjE2MjM5MDIyLCAiZXhwIjogMTYyMjQyMzAyMn0.xxx",
  "token_type": "bearer"
}
```

### Passo 2: Usar o Token (GET de funcionários)
```bash
curl -X GET http://localhost:8000/funcionario/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

Response (200):
```json
{
  "msg": "funcionario get todos executado",
  "usuario_id": 1
}
```

### Passo 3: Tentar acesso sem permissão
```bash
# Usuário com grupo 2 tentando listar funcionários (requer grupo 1)
curl -X GET http://localhost:8000/funcionario/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

Response (403):
```json
{
  "detail": "Acesso negado. Grupos permitidos: [1]"
}
```

### Passo 4: Renovar Token (quando expirar)
```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "seu_refresh_token_aqui"
  }'
```

---

## CONFIGURAÇÃO

### Arquivo `.env`
```
HOST=0.0.0.0
PORT=8000
RELOAD=True
JWT_SECRET_KEY=sua-chave-secreta-muito-segura-mude-isto-em-producao
```

### Variáveis em `settings.py`
- `ACCESS_TOKEN_EXPIRE_MINUTES = 15` - Validade do access token
- `REFRESH_TOKEN_EXPIRE_DAYS = 7` - Validade do refresh token

---

## ARQUIVOS CRIADOS/MODIFICADOS

### Novos Arquivos:
- `src/auth.py` - Lógica de tokens JWT
- `src/dependencies.py` - Funções de injeção de dependência
- `src/routers/AuthRouter.py` - Rotas de autenticação
- `.env` - Variáveis de ambiente

### Arquivos Modificados:
- `src/settings.py` - Adicionadas configurações JWT
- `src/main.py` - Incluído router de auth
- `src/routers/FuncionarioRouter.py` - Adicionada segurança
- `src/routers/ClienteRouter.py` - Adicionada segurança
- `src/routers/ProdutoRouter.py` - Adicionada segurança
- `requirements.txt` - Adicionado PyJWT

---

## PRÓXIMOS PASSOS

1. **Integração com Banco de Dados**: Substituir a validação fictícia de login com queries reais
2. **Blacklist de Tokens**: Implementar sistema de logout com Redis/banco de dados
3. **Hash de Senhas**: Usar bcrypt para criptografar senhas antes de armazenar
4. **Refresh Token Rotation**: Invalidar refresh tokens antigos após usar
5. **Rate Limiting**: Adicionar limite de tentativas de login
6. **Logs de Auditoria**: Registrar ações de usuários autenticados

---

## TESTAR NO SWAGGER UI

Acesse: `http://localhost:8000/docs`

Todos os endpoints estão documentados e com a opção "Authorize" para adicionar tokens Bearer.
