# 📸 Como Adicionar Sua Imagem de Perfil

## ⚠️ Importante para Entrega da Atividade

A página de perfil está pronta para exibir sua imagem! Basta seguir os passos abaixo:

---

## 📁 Passo 1: Salvar a Imagem

**Salve sua foto no seguinte caminho:**

```
c:\Users\Nicolas\Desktop\faculdade\comandas_api\frontend\public\avatar.jpg
```

### Formato:
- **Nome do arquivo**: `avatar.jpg` (ou `.png`, `.jpeg`)
- **Pasta**: `public`
- **Tamanho recomendado**: 500x500px (quadrada)
- **Formato**: JPG, PNG ou JPEG

---

## 🖼️ Passo 2: Verificar se a Imagem Aparece

Após salvar a imagem, a mesma será exibida em:

### 🎯 **NAVBAR** (em todas as páginas)
- Avatar no canto superior direito
- Avatar no menu lateral (mobile)
- Ao clicar no avatar, abre menu com opção "Meu Perfil"

### 🎯 **PÁGINA DE PERFIL** (`/perfil`)
- Card grande com sua foto destaque
- Nome do usuário: `abc`
- Nível de acesso e status
- Informações de usuário

---

## ✅ Checklist de Atendimento do Requisito

O requisito da atividade pediu:

> "Deve ser obrigatoriamente incorporada à interface gráfica da aplicação uma imagem contendo o seu rosto."

✅ **Implementação:**
- ✅ Página de Perfil criada (`/perfil`)
- ✅ Avatar grande na página de perfil
- ✅ Avatar na Navbar (aparece em todas as telas)
- ✅ Avatar no menu lateral (mobile)
- ✅ Nome do usuário exibido em múltiplos lugares
- ✅ Acesso via menu de navegação

---

## 📱 Onde a Imagem Aparece

### Desktop
1. **Navbar** - Canto superior direito (avatar pequeno)
2. **Menu dropdown** - Ao clicar no avatar
3. **Página /perfil** - Avatar grande e destaque

### Mobile
1. **Navbar** - Avatar à esquerda (após hamburger menu)
2. **Menu lateral** - Avatar no topo
3. **Página /perfil** - Avatar grande e destaque

---

## 🎨 Exemplo de Estrutura

```
frontend/
└── public/
    ├── avatar.jpg ← 🎯 COLOQUE SUA IMAGEM AQUI
    └── vite.svg
```

---

## 🚀 Próximos Passos

1. **Salve sua foto** em `public/avatar.jpg`
2. **Rode `npm run dev`**
3. **Acesse `http://localhost:3000`**
4. **Faça login** com `abc/bolinhas`
5. **Sua foto aparecerá** na navbar e em `/perfil`

---

## 💡 Dicas

- Se a imagem não aparecer, limpe o cache do navegador (Ctrl+Shift+Delete)
- Verifique se o nome do arquivo é exatamente `avatar.jpg`
- A imagem pode ser JPG, PNG ou JPEG
- Imagens quadradas funcionam melhor (500x500px)

---

## ✨ Resultado Final

Após salvar a imagem:

- ✅ **Navbar**: Sua foto aparece em todas as telas
- ✅ **Perfil**: Página dedicada com sua foto em destaque
- ✅ **Menu**: Opção "Meu Perfil" para acessar a página
- ✅ **Responsividade**: Funciona em mobile e desktop

---

**Sua aplicação está pronta! Basta adicionar a imagem e fazer o teste! 🎉**
