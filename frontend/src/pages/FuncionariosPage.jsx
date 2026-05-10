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
  Grid,
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
import { funcionariosService } from '../services/funcionariosService'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import { EmptyState } from '../components/ui/EmptyState'
import { SnackbarAlert } from '../components/ui/SnackbarAlert'
import { ConfirmDialog } from '../components/ui/ConfirmDialog'
import { useValidationRules } from '../hooks/useValidationRules'
import { useSnackbar } from '../hooks/useSnackbar'

export const FuncionariosPage = () => {
  const [funcionarios, setFuncionarios] = useState([])
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
      matricula: '',
      senha: ''
    }
  })
  const { getRule } = useValidationRules()
  const snackbar = useSnackbar()

  useEffect(() => {
    fetchFuncionarios()
  }, [])

  const fetchFuncionarios = async () => {
    setLoading(true)
    const result = await funcionariosService.getAll()
    if (result.success) {
      setFuncionarios(result.data || [])
    } else {
      snackbar.showSnackbar(result.error || 'Erro ao carregar funcionários', 'error')
    }
    setLoading(false)
  }

  const handleOpenDialog = (funcionario = null) => {
    if (funcionario) {
      setEditingId(funcionario.id)
      reset({
        nome: funcionario.nome || '',
        cpf: funcionario.cpf || '',
        email: funcionario.email || '',
        matricula: funcionario.matricula || '',
        senha: ''
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
        result = await funcionariosService.update(editingId, data)
      } else {
        result = await funcionariosService.create(data)
      }

      if (result.success) {
        snackbar.showSnackbar(
          editingId ? 'Funcionário atualizado com sucesso!' : 'Funcionário criado com sucesso!',
          'success'
        )
        handleCloseDialog()
        await fetchFuncionarios()
      } else {
        snackbar.showSnackbar(result.error || 'Erro ao salvar funcionário', 'error')
      }
    } catch (error) {
      snackbar.showSnackbar('Erro ao salvar funcionário', 'error')
    }
  }

  const handleDelete = async (id) => {
    const result = await funcionariosService.delete(id)
    if (result.success) {
      snackbar.showSnackbar('Funcionário deletado com sucesso!', 'success')
      await fetchFuncionarios()
    } else {
      snackbar.showSnackbar(result.error || 'Erro ao deletar funcionário', 'error')
    }
    setConfirmDialog({ open: false, id: null })
  }

  const filteredFuncionarios = funcionarios.filter(f =>
    f.nome?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    f.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    f.cpf?.includes(searchTerm)
  )

  if (loading) {
    return <LoadingSpinner message="Carregando funcionários..." />
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Gerenciamento de Funcionários
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => handleOpenDialog()}
            sx={{
              background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)'
            }}
          >
            Novo Funcionário
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
        {filteredFuncionarios.length > 0 ? (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                  <TableCell sx={{ fontWeight: 700 }}>Nome</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>CPF</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>Email</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>Matrícula</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 700 }}>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredFuncionarios.map((funcionario) => (
                  <TableRow
                    key={funcionario.id}
                    sx={{
                      '&:hover': { backgroundColor: '#f9f9f9' },
                      '&:nth-of-type(even)': { backgroundColor: '#fafafa' }
                    }}
                  >
                    <TableCell sx={{ fontWeight: 500 }}>{funcionario.nome}</TableCell>
                    <TableCell>{funcionario.cpf}</TableCell>
                    <TableCell>{funcionario.email}</TableCell>
                    <TableCell>{funcionario.matricula}</TableCell>
                    <TableCell align="center">
                      <Tooltip title="Editar">
                        <IconButton
                          size="small"
                          onClick={() => handleOpenDialog(funcionario)}
                          sx={{ color: '#1976d2' }}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Deletar">
                        <IconButton
                          size="small"
                          onClick={() => setConfirmDialog({ open: true, id: funcionario.id })}
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
            title="Nenhum funcionário encontrado"
            message="Comece adicionando seu primeiro funcionário"
            onAction={() => handleOpenDialog()}
            actionLabel="Adicionar Funcionário"
          />
        )}

        {/* Dialog de Formulário */}
        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle sx={{ fontWeight: 600 }}>
            {editingId ? 'Editar Funcionário' : 'Novo Funcionário'}
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
                name="matricula"
                control={control}
                rules={getRule('matricula')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Matrícula"
                    margin="normal"
                    error={!!errors.matricula}
                    helperText={errors.matricula?.message}
                  />
                )}
              />

              <Controller
                name="senha"
                control={control}
                rules={getRule('senha')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Senha"
                    type="password"
                    margin="normal"
                    error={!!errors.senha}
                    helperText={errors.senha?.message}
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
              sx={{ background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)' }}
            >
              {editingId ? 'Atualizar' : 'Criar'}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Dialog de Confirmação */}
        <ConfirmDialog
          open={confirmDialog.open}
          title="Confirmar Exclusão"
          message="Tem certeza que deseja deletar este funcionário?"
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
