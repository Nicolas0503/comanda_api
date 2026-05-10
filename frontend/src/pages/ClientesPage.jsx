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
  Tooltip
} from '@mui/material'
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon
} from '@mui/icons-material'
import { useForm, Controller } from 'react-hook-form'
import { clientesService } from '../services/clientesService'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import { EmptyState } from '../components/ui/EmptyState'
import { SnackbarAlert } from '../components/ui/SnackbarAlert'
import { ConfirmDialog } from '../components/ui/ConfirmDialog'
import { useValidationRules } from '../hooks/useValidationRules'
import { useSnackbar } from '../hooks/useSnackbar'

export const ClientesPage = () => {
  const [clientes, setClientes] = useState([])
  const [loading, setLoading] = useState(true)
  const [openDialog, setOpenDialog] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [confirmDialog, setConfirmDialog] = useState({ open: false, id: null })
  const [searchTerm, setSearchTerm] = useState('')
  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      nome: '',
      cpf: '',
      email: '',
      telefone: '',
      endereco: '',
      cidade: '',
      estado: ''
    }
  })
  const { getRule } = useValidationRules()
  const snackbar = useSnackbar()

  useEffect(() => {
    fetchClientes()
  }, [])

  const fetchClientes = async () => {
    setLoading(true)
    const result = await clientesService.getAll()
    if (result.success) {
      setClientes(result.data || [])
    } else {
      snackbar.showSnackbar(result.error || 'Erro ao carregar clientes', 'error')
    }
    setLoading(false)
  }

  const handleOpenDialog = (cliente = null) => {
    if (cliente) {
      setEditingId(cliente.id)
      reset({
        nome: cliente.nome || '',
        cpf: cliente.cpf || '',
        email: cliente.email || '',
        telefone: cliente.telefone || '',
        endereco: cliente.endereco || '',
        cidade: cliente.cidade || '',
        estado: cliente.estado || ''
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
        result = await clientesService.update(editingId, data)
      } else {
        result = await clientesService.create(data)
      }

      if (result.success) {
        snackbar.showSnackbar(
          editingId ? 'Cliente atualizado com sucesso!' : 'Cliente criado com sucesso!',
          'success'
        )
        handleCloseDialog()
        await fetchClientes()
      } else {
        snackbar.showSnackbar(result.error || 'Erro ao salvar cliente', 'error')
      }
    } catch (error) {
      snackbar.showSnackbar('Erro ao salvar cliente', 'error')
    }
  }

  const handleDelete = async (id) => {
    const result = await clientesService.delete(id)
    if (result.success) {
      snackbar.showSnackbar('Cliente deletado com sucesso!', 'success')
      await fetchClientes()
    } else {
      snackbar.showSnackbar(result.error || 'Erro ao deletar cliente', 'error')
    }
    setConfirmDialog({ open: false, id: null })
  }

  const filteredClientes = clientes.filter(c =>
    c.nome?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.cpf?.includes(searchTerm)
  )

  if (loading) {
    return <LoadingSpinner message="Carregando clientes..." />
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Gerenciamento de Clientes
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => handleOpenDialog()}
            sx={{ background: 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)' }}
          >
            Novo Cliente
          </Button>
        </Box>

        {/* Barra de Pesquisa */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <TextField
              fullWidth
              placeholder="Pesquise por nome, email ou CPF..."
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
        {filteredClientes.length > 0 ? (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                  <TableCell sx={{ fontWeight: 700 }}>Nome</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>CPF</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>Email</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>Telefone</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>Cidade</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 700 }}>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredClientes.map((cliente) => (
                  <TableRow
                    key={cliente.id}
                    sx={{
                      '&:hover': { backgroundColor: '#f9f9f9' },
                      '&:nth-of-type(even)': { backgroundColor: '#fafafa' }
                    }}
                  >
                    <TableCell sx={{ fontWeight: 500 }}>{cliente.nome}</TableCell>
                    <TableCell>{cliente.cpf}</TableCell>
                    <TableCell>{cliente.email}</TableCell>
                    <TableCell>{cliente.telefone}</TableCell>
                    <TableCell>{cliente.cidade}</TableCell>
                    <TableCell align="center">
                      <Tooltip title="Editar">
                        <IconButton
                          size="small"
                          onClick={() => handleOpenDialog(cliente)}
                          sx={{ color: '#4caf50' }}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Deletar">
                        <IconButton
                          size="small"
                          onClick={() => setConfirmDialog({ open: true, id: cliente.id })}
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
            title="Nenhum cliente encontrado"
            message="Comece adicionando seu primeiro cliente"
            onAction={() => handleOpenDialog()}
            actionLabel="Adicionar Cliente"
          />
        )}

        {/* Dialog de Formulário */}
        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle sx={{ fontWeight: 600 }}>
            {editingId ? 'Editar Cliente' : 'Novo Cliente'}
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
                name="cpf"
                control={control}
                rules={getRule('cpf')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="CPF"
                    margin="normal"
                    error={!!errors.cpf}
                    helperText={errors.cpf?.message}
                  />
                )}
              />

              <Controller
                name="email"
                control={control}
                rules={getRule('email')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Email"
                    type="email"
                    margin="normal"
                    error={!!errors.email}
                    helperText={errors.email?.message}
                  />
                )}
              />

              <Controller
                name="telefone"
                control={control}
                rules={getRule('telefone')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Telefone"
                    margin="normal"
                    error={!!errors.telefone}
                    helperText={errors.telefone?.message}
                  />
                )}
              />

              <Controller
                name="endereco"
                control={control}
                rules={getRule('endereco')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Endereço"
                    margin="normal"
                    error={!!errors.endereco}
                    helperText={errors.endereco?.message}
                  />
                )}
              />

              <Controller
                name="cidade"
                control={control}
                rules={getRule('cidade')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Cidade"
                    margin="normal"
                    error={!!errors.cidade}
                    helperText={errors.cidade?.message}
                  />
                )}
              />

              <Controller
                name="estado"
                control={control}
                rules={getRule('estado')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Estado"
                    margin="normal"
                    error={!!errors.estado}
                    helperText={errors.estado?.message}
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
              sx={{ background: 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)' }}
            >
              {editingId ? 'Atualizar' : 'Criar'}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Dialog de Confirmação */}
        <ConfirmDialog
          open={confirmDialog.open}
          title="Confirmar Exclusão"
          message="Tem certeza que deseja deletar este cliente?"
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
