import React, { useState, useEffect } from 'react'
import {
  Container,
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Dialog,
  TextField,
  DialogTitle,
  DialogContent,
  DialogActions,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material'
import {
  Add as AddIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  AttachMoney as AttachMoneyIcon,
  LocalAtm as LocalAtmIcon
} from '@mui/icons-material'
import { useForm, Controller } from 'react-hook-form'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import { SnackbarAlert } from '../components/ui/SnackbarAlert'
import { StatCard } from '../components/ui/StatCard'
import { useSnackbar } from '../hooks/useSnackbar'

export const CaixaPage = () => {
  const [caixa, setCaixa] = useState({
    saldoAtual: 0,
    receitas: 0,
    despesas: 0,
    movimentacoes: []
  })
  const [loading, setLoading] = useState(false)
  const [openDialog, setOpenDialog] = useState(false)
  const { control, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      tipo: 'receita',
      descricao: '',
      valor: '',
      categoria: ''
    }
  })
  const snackbar = useSnackbar()

  useEffect(() => {
    fetchCaixaData()
  }, [])

  const fetchCaixaData = async () => {
    setLoading(true)
    // Simulando dados de caixa
    setCaixa({
      saldoAtual: 5430.50,
      receitas: 10850.00,
      despesas: 5419.50,
      movimentacoes: [
        {
          id: 1,
          tipo: 'receita',
          descricao: 'Venda de comandas',
          valor: 2500.00,
          categoria: 'Vendas',
          data: '2026-05-10'
        },
        {
          id: 2,
          tipo: 'despesa',
          descricao: 'Aluguel',
          valor: 2000.00,
          categoria: 'Aluguel',
          data: '2026-05-01'
        },
        {
          id: 3,
          tipo: 'receita',
          descricao: 'Desconto aplicado',
          valor: 150.00,
          categoria: 'Diverso',
          data: '2026-05-09'
        },
        {
          id: 4,
          tipo: 'despesa',
          descricao: 'Material de limpeza',
          valor: 300.00,
          categoria: 'Suprimentos',
          data: '2026-05-08'
        },
        {
          id: 5,
          tipo: 'receita',
          descricao: 'Comissão de vendedor',
          valor: 1200.00,
          categoria: 'Vendas',
          data: '2026-05-07'
        }
      ]
    })
    setLoading(false)
  }

  const handleOpenDialog = () => {
    setOpenDialog(true)
  }

  const handleCloseDialog = () => {
    setOpenDialog(false)
    reset()
  }

  const onSubmit = async (data) => {
    try {
      const novaMovimentacao = {
        id: caixa.movimentacoes.length + 1,
        ...data,
        data: new Date().toISOString().split('T')[0]
      }

      const novoSaldo =
        data.tipo === 'receita'
          ? caixa.saldoAtual + parseFloat(data.valor)
          : caixa.saldoAtual - parseFloat(data.valor)

      setCaixa({
        ...caixa,
        saldoAtual: novoSaldo,
        receitas:
          data.tipo === 'receita'
            ? caixa.receitas + parseFloat(data.valor)
            : caixa.receitas,
        despesas:
          data.tipo === 'despesa'
            ? caixa.despesas + parseFloat(data.valor)
            : caixa.despesas,
        movimentacoes: [novaMovimentacao, ...caixa.movimentacoes]
      })

      snackbar.showSnackbar('Movimentação registrada com sucesso!', 'success')
      handleCloseDialog()
    } catch (error) {
      snackbar.showSnackbar('Erro ao registrar movimentação', 'error')
    }
  }

  if (loading) {
    return <LoadingSpinner message="Carregando dados do caixa..." />
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Relatório de Caixa
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleOpenDialog}
            sx={{ background: 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)' }}
          >
            Nova Movimentação
          </Button>
        </Box>

        {/* Cards de Resumo */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={4} lg={3}>
            <StatCard
              title="Saldo Atual"
              value={`R$ ${caixa.saldoAtual.toFixed(2)}`}
              icon={LocalAtmIcon}
              color="#4caf50"
            />
          </Grid>

          <Grid item xs={12} sm={6} md={4} lg={3}>
            <StatCard
              title="Total de Receitas"
              value={`R$ ${caixa.receitas.toFixed(2)}`}
              icon={TrendingUpIcon}
              color="#4caf50"
            />
          </Grid>

          <Grid item xs={12} sm={6} md={4} lg={3}>
            <StatCard
              title="Total de Despesas"
              value={`R$ ${caixa.despesas.toFixed(2)}`}
              icon={TrendingDownIcon}
              color="#f44336"
            />
          </Grid>

          <Grid item xs={12} sm={6} md={4} lg={3}>
            <StatCard
              title="Lucro Líquido"
              value={`R$ ${(caixa.receitas - caixa.despesas).toFixed(2)}`}
              icon={AttachMoneyIcon}
              color="#1976d2"
            />
          </Grid>
        </Grid>

        {/* Resumo de Movimentações */}
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h5" sx={{ fontWeight: 600, mb: 3 }}>
              Últimas Movimentações
            </Typography>

            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                    <TableCell sx={{ fontWeight: 700 }}>Data</TableCell>
                    <TableCell sx={{ fontWeight: 700 }}>Tipo</TableCell>
                    <TableCell sx={{ fontWeight: 700 }}>Descrição</TableCell>
                    <TableCell sx={{ fontWeight: 700 }}>Categoria</TableCell>
                    <TableCell align="right" sx={{ fontWeight: 700 }}>Valor</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {caixa.movimentacoes.map((mov, idx) => (
                    <TableRow
                      key={mov.id}
                      sx={{
                        '&:hover': { backgroundColor: '#f9f9f9' },
                        '&:nth-of-type(even)': { backgroundColor: '#fafafa' }
                      }}
                    >
                      <TableCell>{mov.data}</TableCell>
                      <TableCell>
                        <Chip
                          label={mov.tipo === 'receita' ? 'Receita' : 'Despesa'}
                          size="small"
                          color={mov.tipo === 'receita' ? 'success' : 'error'}
                          variant="filled"
                        />
                      </TableCell>
                      <TableCell sx={{ fontWeight: 500 }}>{mov.descricao}</TableCell>
                      <TableCell>
                        <Chip
                          label={mov.categoria}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell
                        align="right"
                        sx={{
                          fontWeight: 600,
                          color: mov.tipo === 'receita' ? '#4caf50' : '#f44336'
                        }}
                      >
                        {mov.tipo === 'receita' ? '+' : '-'} R$ {mov.valor.toFixed(2)}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>

        {/* Dialog de Nova Movimentação */}
        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle sx={{ fontWeight: 600 }}>
            Nova Movimentação
          </DialogTitle>
          <DialogContent sx={{ pt: 2 }}>
            <form>
              <FormControl fullWidth margin="normal">
                <Controller
                  name="tipo"
                  control={control}
                  render={({ field }) => (
                    <div>
                      <InputLabel>Tipo</InputLabel>
                      <Select
                        {...field}
                        label="Tipo"
                      >
                        <MenuItem value="receita">Receita</MenuItem>
                        <MenuItem value="despesa">Despesa</MenuItem>
                      </Select>
                    </div>
                  )}
                />
              </FormControl>

              <Controller
                name="descricao"
                control={control}
                rules={{ required: 'Descrição é obrigatória' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Descrição"
                    margin="normal"
                    error={!!errors.descricao}
                    helperText={errors.descricao?.message}
                  />
                )}
              />

              <Controller
                name="categoria"
                control={control}
                rules={{ required: 'Categoria é obrigatória' }}
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
                name="valor"
                control={control}
                rules={{
                  required: 'Valor é obrigatório',
                  min: { value: 0.01, message: 'Valor deve ser maior que 0' }
                }}
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
            </form>
          </DialogContent>
          <DialogActions sx={{ padding: 2 }}>
            <Button onClick={handleCloseDialog} variant="outlined">
              Cancelar
            </Button>
            <Button
              onClick={handleSubmit(onSubmit)}
              variant="contained"
              sx={{ background: 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)' }}
            >
              Registrar
            </Button>
          </DialogActions>
        </Dialog>

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
