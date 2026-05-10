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
  Chip,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material'
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  Print as PrintIcon
} from '@mui/icons-material'
import { useForm, Controller } from 'react-hook-form'
import { comandasService } from '../services/comandasService'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import { EmptyState } from '../components/ui/EmptyState'
import { SnackbarAlert } from '../components/ui/SnackbarAlert'
import { ConfirmDialog } from '../components/ui/ConfirmDialog'
import { useValidationRules } from '../hooks/useValidationRules'
import { useSnackbar } from '../hooks/useSnackbar'

export const ComandasPage = () => {
  const [comandas, setComandas] = useState([])
  const [loading, setLoading] = useState(true)
  const [openDialog, setOpenDialog] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [confirmDialog, setConfirmDialog] = useState({ open: false, id: null })
  const [searchTerm, setSearchTerm] = useState('')
  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      numero: '',
      cliente: '',
      descricao: '',
      valor: '',
      status: 'aberta'
    }
  })
  const { getRule } = useValidationRules()
  const snackbar = useSnackbar()

  useEffect(() => {
    fetchComandas()
  }, [])

  const fetchComandas = async () => {
    setLoading(true)
    const result = await comandasService.getAll()
    if (result.success) {
      setComandas(result.data || [])
    } else {
      snackbar.showSnackbar(result.error || 'Erro ao carregar comandas', 'error')
    }
    setLoading(false)
  }

  const handleOpenDialog = (comanda = null) => {
    if (comanda) {
      setEditingId(comanda.id)
      reset({
        numero: comanda.numero || '',
        cliente: comanda.cliente || '',
        descricao: comanda.descricao || '',
        valor: comanda.valor || '',
        status: comanda.status || 'aberta'
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
        result = await comandasService.update(editingId, data)
      } else {
        result = await comandasService.create(data)
      }

      if (result.success) {
        snackbar.showSnackbar(
          editingId ? 'Comanda atualizada com sucesso!' : 'Comanda criada com sucesso!',
          'success'
        )
        handleCloseDialog()
        await fetchComandas()
      } else {
        snackbar.showSnackbar(result.error || 'Erro ao salvar comanda', 'error')
      }
    } catch (error) {
      snackbar.showSnackbar('Erro ao salvar comanda', 'error')
    }
  }

  const handleDelete = async (id) => {
    const result = await comandasService.delete(id)
    if (result.success) {
      snackbar.showSnackbar('Comanda deletada com sucesso!', 'success')
      await fetchComandas()
    } else {
      snackbar.showSnackbar(result.error || 'Erro ao deletar comanda', 'error')
    }
    setConfirmDialog({ open: false, id: null })
  }

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'aberta':
        return 'warning'
      case 'fechada':
        return 'success'
      case 'paga':
        return 'success'
      case 'cancelada':
        return 'error'
      default:
        return 'default'
    }
  }

  const filteredComandas = comandas.filter(c =>
    c.numero?.toString().includes(searchTerm) ||
    c.cliente?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.status?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return <LoadingSpinner message="Carregando comandas..." />
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Gerenciamento de Comandas
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => handleOpenDialog()}
            sx={{ background: 'linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%)' }}
          >
            Nova Comanda
          </Button>
        </Box>

        {/* Barra de Pesquisa */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <TextField
              fullWidth
              placeholder="Pesquise por número, cliente ou status..."
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
        {filteredComandas.length > 0 ? (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                  <TableCell sx={{ fontWeight: 700 }}>Número</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>Cliente</TableCell>
                  <TableCell sx={{ fontWeight: 700 }}>Descrição</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700 }}>Valor</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 700 }}>Status</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 700 }}>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredComandas.map((comanda) => (
                  <TableRow
                    key={comanda.id}
                    sx={{
                      '&:hover': { backgroundColor: '#f9f9f9' },
                      '&:nth-of-type(even)': { backgroundColor: '#fafafa' }
                    }}
                  >
                    <TableCell sx={{ fontWeight: 700 }}># {comanda.numero}</TableCell>
                    <TableCell sx={{ fontWeight: 500 }}>{comanda.cliente}</TableCell>
                    <TableCell sx={{ maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {comanda.descricao}
                    </TableCell>
                    <TableCell align="right" sx={{ fontWeight: 600, color: '#9c27b0' }}>
                      R$ {parseFloat(comanda.valor || 0).toFixed(2)}
                    </TableCell>
                    <TableCell align="center">
                      <Chip
                        label={comanda.status}
                        size="small"
                        color={getStatusColor(comanda.status)}
                        variant="filled"
                      />
                    </TableCell>
                    <TableCell align="center">
                      <Tooltip title="Imprimir">
                        <IconButton
                          size="small"
                          sx={{ color: '#2196f3' }}
                        >
                          <PrintIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Editar">
                        <IconButton
                          size="small"
                          onClick={() => handleOpenDialog(comanda)}
                          sx={{ color: '#9c27b0' }}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Deletar">
                        <IconButton
                          size="small"
                          onClick={() => setConfirmDialog({ open: true, id: comanda.id })}
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
            title="Nenhuma comanda encontrada"
            message="Comece adicionando sua primeira comanda"
            onAction={() => handleOpenDialog()}
            actionLabel="Adicionar Comanda"
          />
        )}

        {/* Dialog de Formulário */}
        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle sx={{ fontWeight: 600 }}>
            {editingId ? 'Editar Comanda' : 'Nova Comanda'}
          </DialogTitle>
          <DialogContent sx={{ pt: 2 }}>
            <form>
              <Controller
                name="numero"
                control={control}
                rules={{ required: 'Número é obrigatório' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Número"
                    type="number"
                    margin="normal"
                    error={!!errors.numero}
                    helperText={errors.numero?.message}
                  />
                )}
              />

              <Controller
                name="cliente"
                control={control}
                rules={{ required: 'Cliente é obrigatório' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Cliente"
                    margin="normal"
                    error={!!errors.cliente}
                    helperText={errors.cliente?.message}
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
                name="valor"
                control={control}
                rules={getRule('valor')}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Valor (R$)"
                    type="number"
                    margin="normal"
                    inputProps={{ step: '0.01' }}
                    error={!!errors.valor}
                    helperText={errors.valor?.message}
                  />
                )}
              />

              <FormControl fullWidth margin="normal">
                <Controller
                  name="status"
                  control={control}
                  render={({ field }) => (
                    <div>
                      <InputLabel>Status</InputLabel>
                      <Select
                        {...field}
                        label="Status"
                      >
                        <MenuItem value="aberta">Aberta</MenuItem>
                        <MenuItem value="fechada">Fechada</MenuItem>
                        <MenuItem value="paga">Paga</MenuItem>
                        <MenuItem value="cancelada">Cancelada</MenuItem>
                      </Select>
                    </div>
                  )}
                />
              </FormControl>
            </form>
          </DialogContent>
          <DialogActions sx={{ padding: 2 }}>
            <Button onClick={handleCloseDialog} variant="outlined">
              Cancelar
            </Button>
            <Button
              onClick={handleSubmit(onSubmit)}
              variant="contained"
              sx={{ background: 'linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%)' }}
            >
              {editingId ? 'Atualizar' : 'Criar'}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Dialog de Confirmação */}
        <ConfirmDialog
          open={confirmDialog.open}
          title="Confirmar Exclusão"
          message="Tem certeza que deseja deletar esta comanda?"
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
