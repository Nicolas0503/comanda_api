import React, { useState, useEffect } from 'react'
import {
  Container,
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Dialog,
  TextField,
  DialogTitle,
  DialogContent,
  DialogActions,
  Card,
  CardContent,
  IconButton,
  Tooltip,
  Chip
} from '@mui/material'
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon
} from '@mui/icons-material'
import { useForm, Controller } from 'react-hook-form'
import { produtosService } from '../services/produtosService'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import { EmptyState } from '../components/ui/EmptyState'
import { SnackbarAlert } from '../components/ui/SnackbarAlert'
import { ConfirmDialog } from '../components/ui/ConfirmDialog'
import { useValidationRules } from '../hooks/useValidationRules'
import { useSnackbar } from '../hooks/useSnackbar'

export const ProdutosPage = () => {
  const [produtos, setProdutos] = useState([])
  const [loading, setLoading] = useState(true)
  const [openDialog, setOpenDialog] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [confirmDialog, setConfirmDialog] = useState({ open: false, id: null })
  const [searchTerm, setSearchTerm] = useState('')
  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      nome: '',
      descricao: '',
      preco: '',
      categoria: '',
      estoque: ''
    }
  })
  const { getRule } = useValidationRules()
  const snackbar = useSnackbar()

  useEffect(() => {
    fetchProdutos()
  }, [])

  const fetchProdutos = async () => {
    setLoading(true)
    const result = await produtosService.getAll()
    if (result.success) {
      setProdutos(result.data || [])
    } else {
      snackbar.showSnackbar(result.error || 'Erro ao carregar produtos', 'error')
    }
    setLoading(false)
  }

  const handleOpenDialog = (produto = null) => {
    if (produto) {
      setEditingId(produto.id)
      reset({
        nome: produto.nome || '',
        descricao: produto.descricao || '',
        preco: produto.preco || '',
        categoria: produto.categoria || '',
        estoque: produto.estoque || ''
      })
    } else {
      setEditingId(null)
      reset()
    }
    setOpenDialog(true)
  }

  const handleCloseDialog = () => {
    setOpenDialog(false)
    setEditingId(null)
    reset()
  }

  const onSubmit = async (data) => {
    try {
      let result
      if (editingId) {
        result = await produtosService.update(editingId, data)
      } else {
        result = await produtosService.create(data)
      }

      if (result.success) {
        snackbar.showSnackbar(
          editingId ? 'Produto atualizado com sucesso!' : 'Produto criado com sucesso!',
          'success'
        )
        handleCloseDialog()
        await fetchProdutos()
      } else {
        snackbar.showSnackbar(result.error || 'Erro ao salvar produto', 'error')
      }
    } catch (error) {
      snackbar.showSnackbar('Erro ao salvar produto', 'error')
    }
  }

  const handleDelete = async (id) => {
    const result = await produtosService.delete(id)
    if (result.success) {
      snackbar.showSnackbar('Produto deletado com sucesso!', 'success')
      await fetchProdutos()
    } else {
      snackbar.showSnackbar(result.error || 'Erro ao deletar produto', 'error')
    }
    setConfirmDialog({ open: false, id: null })
  }

  const filteredProdutos = produtos.filter(p =>
    p.nome?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.categoria?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return <LoadingSpinner message="Carregando produtos..." />
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Gerenciamento de Produtos
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => handleOpenDialog()}
            sx={{ background: 'linear-gradient(135deg, #ff9800 0%, #f57c00 100%)' }}
          >
            Novo Produto
          </Button>
        </Box>

        {/* Barra de Pesquisa */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <TextField
              fullWidth
              placeholder="Pesquise por nome ou categoria..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: <SearchIcon sx={{ mr: 1, color: '#999' }} />
              }}
              variant="outlined"
              size="small"
            />
          </CardContent>
        </Card>

        {/* Tabela */}
        {filteredProdutos.length > 0 ? (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                  <TableCell sx={{ fontWeight: 700 }}>Nome</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>Categoria</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>Descrição</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700 }}>Preço</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 700 }}>Estoque</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 700 }}>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredProdutos.map((produto) => (
                  <TableRow
                    key={produto.id}
                    sx={{
                      '&:hover': { backgroundColor: '#f9f9f9' },
                      '&:nth-of-type(even)': { backgroundColor: '#fafafa' }
                    }}
                  >
                    <TableCell sx={{ fontWeight: 500 }}>{produto.nome}</TableCell>
                    <TableCell>
                      <Chip
                        label={produto.categoria}
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {produto.descricao}
                    </TableCell>
                    <TableCell align="right" sx={{ fontWeight: 600, color: '#4caf50' }}>
                      R$ {parseFloat(produto.preco || 0).toFixed(2)}
                    </TableCell>
                    <TableCell align="center">
                      <Chip
                        label={`${produto.estoque || 0} un`}
                        size="small"
                        color={produto.estoque > 10 ? 'success' : 'warning'}
                        variant="filled"
                      />
                    </TableCell>
                    <TableCell align="center">
                      <Tooltip title="Editar">
                        <IconButton
                          size="small"
                          onClick={() => handleOpenDialog(produto)}
                          sx={{ color: '#ff9800' }}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Deletar">
                        <IconButton
                          size="small"
                          onClick={() => setConfirmDialog({ open: true, id: produto.id })}
                          sx={{ color: '#f44336' }}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        ) : (
          <EmptyState
            title="Nenhum produto encontrado"
            message="Comece adicionando seu primeiro produto"
            onAction={() => handleOpenDialog()}
            actionLabel="Adicionar Produto"
          />
        )}

        {/* Dialog de Formulário */}
        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle sx={{ fontWeight: 600 }}>
            {editingId ? 'Editar Produto' : 'Novo Produto'}
          </DialogTitle>
          <DialogContent sx={{ pt: 2 }}>
            <form>
              <Controller
                name="nome"
                control={control}
                rules={getRule('nome')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Nome"
                    margin="normal"
                    error={!!errors.nome}
                    helperText={errors.nome?.message}
                  />
                )}
              />

              <Controller
                name="descricao"
                control={control}
                rules={getRule('descricao')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Descrição"
                    margin="normal"
                    multiline
                    rows={3}
                    error={!!errors.descricao}
                    helperText={errors.descricao?.message}
                  />
                )}
              />

              <Controller
                name="preco"
                control={control}
                rules={getRule('valor')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Preço (R$)"
                    type="number"
                    margin="normal"
                    inputProps={{ step: '0.01' }}
                    error={!!errors.preco}
                    helperText={errors.preco?.message}
                  />
                )}
              />

              <Controller
                name="categoria"
                control={control}
                rules={getRule('categoria')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Categoria"
                    margin="normal"
                    error={!!errors.categoria}
                    helperText={errors.categoria?.message}
                  />
                )}
              />

              <Controller
                name="estoque"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Estoque"
                    type="number"
                    margin="normal"
                  />
                )}
              />
            </form>
          </DialogContent>
          <DialogActions sx={{ padding: 2 }}>
            <Button onClick={handleCloseDialog} variant="outlined">
              Cancelar
            </Button>
            <Button
              onClick={handleSubmit(onSubmit)}
              variant="contained"
              sx={{ background: 'linear-gradient(135deg, #ff9800 0%, #f57c00 100%)' }}
            >
              {editingId ? 'Atualizar' : 'Criar'}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Dialog de Confirmação */}
        <ConfirmDialog
          open={confirmDialog.open}
          title="Confirmar Exclusão"
          message="Tem certeza que deseja deletar este produto?"
          onConfirm={() => handleDelete(confirmDialog.id)}
          onCancel={() => setConfirmDialog({ open: false, id: null })}
          confirmText="Deletar"
          severity="error"
        />

        {/* Snackbar */}
        <SnackbarAlert
          open={snackbar.open}
          message={snackbar.message}
          severity={snackbar.severity}
          onClose={snackbar.closeSnackbar}
        />
      </Box>
    </Container>
  )
}
