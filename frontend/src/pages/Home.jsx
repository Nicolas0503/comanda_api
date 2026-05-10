import React, { useEffect, useState } from 'react'
import {
  Box,
  Grid,
  Typography,
  Card,
  CardContent,
  Button,
  Container,
  Avatar,
  Stack,
  Chip
} from '@mui/material'
import {
  BarChart as BarChartIcon,
  People as PeopleIcon,
  ShoppingCart as ShoppingCartIcon,
  Receipt as ReceiptIcon,
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material'
import { StatCard } from '../components/ui/StatCard'
import { useAuth } from '../hooks/useAuth'

export const Home = () => {
  const { user } = useAuth()
  const [avatarSrc, setAvatarSrc] = useState('/image.png')
  const [stats, setStats] = useState({
    totalFuncionarios: 0,
    totalClientes: 0,
    totalProdutos: 0,
    totalComandas: 0,
    receita: 0
  })

  useEffect(() => {
    // Simulando dados de estatísticas
    setStats({
      totalFuncionarios: 12,
      totalClientes: 47,
      totalProdutos: 120,
      totalComandas: 23,
      receita: 5430.50
    })
  }, [])

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Card
          sx={{
            mb: 4,
            overflow: 'hidden',
            borderRadius: 3,
            background: 'linear-gradient(135deg, rgba(25,118,210,0.12) 0%, rgba(220,0,78,0.10) 100%)',
            border: '1px solid rgba(25,118,210,0.15)'
          }}
        >
          <CardContent>
            <Stack
              direction={{ xs: 'column', md: 'row' }}
              spacing={3}
              alignItems={{ xs: 'flex-start', md: 'center' }}
            >
              <Avatar
                src={avatarSrc}
                alt={user?.username}
                onError={() => setAvatarSrc('/avatar.svg')}
                sx={{
                  width: 92,
                  height: 92,
                  border: '4px solid white',
                  boxShadow: '0 8px 20px rgba(0,0,0,0.12)'
                }}
              >
                {user?.username?.[0]?.toUpperCase() || 'U'}
              </Avatar>

              <Box sx={{ flex: 1 }}>
                <Typography variant="h3" sx={{ fontWeight: 800, mb: 1 }}>
                  Bem-vindo, {user?.username}! 👋
                </Typography>
                <Typography variant="body1" sx={{ color: '#666', mb: 2 }}>
                  Aqui está um resumo do seu negócio.
                </Typography>

                <Stack direction="row" spacing={1} sx={{ flexWrap: 'wrap' }}>
                  <Chip label="Foto do rosto visível" color="primary" />
                  <Chip label="Menu ativo em todas as telas" variant="outlined" />
                  <Chip label="Login: abc / bolinhas" variant="outlined" />
                </Stack>
              </Box>
            </Stack>
          </CardContent>
        </Card>

        {/* Cards de Estatísticas */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={4} lg={2.4}>
            <StatCard
              title="Funcionários"
              value={stats.totalFuncionarios}
              icon={PeopleIcon}
              color="#1976d2"
              trend="+2 este mês"
              trendDirection="up"
            />
          </Grid>

          <Grid item xs={12} sm={6} md={4} lg={2.4}>
            <StatCard
              title="Clientes"
              value={stats.totalClientes}
              icon={PeopleIcon}
              color="#4caf50"
              trend="+5 este mês"
              trendDirection="up"
            />
          </Grid>

          <Grid item xs={12} sm={6} md={4} lg={2.4}>
            <StatCard
              title="Produtos"
              value={stats.totalProdutos}
              icon={ShoppingCartIcon}
              color="#ff9800"
              trend="+8 novos"
              trendDirection="up"
            />
          </Grid>

          <Grid item xs={12} sm={6} md={4} lg={2.4}>
            <StatCard
              title="Comandas"
              value={stats.totalComandas}
              icon={ReceiptIcon}
              color="#9c27b0"
              trend="-2 abertas"
              trendDirection="down"
            />
          </Grid>

          <Grid item xs={12} sm={6} md={4} lg={2.4}>
            <StatCard
              title="Receita"
              value={`R$ ${stats.receita.toFixed(2)}`}
              icon={TrendingUpIcon}
              color="#f44336"
              trend="+12% hoje"
              trendDirection="up"
            />
          </Grid>
        </Grid>

        {/* Seção de Atalhos */}
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h5" sx={{ fontWeight: 600, mb: 3 }}>
              Atalhos Rápidos
            </Typography>
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Card
              sx={{
                height: '100%',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: '0 12px 32px rgba(0, 0, 0, 0.15)'
                }
              }}
            >
              <CardContent sx={{ textAlign: 'center', py: 3 }}>
                <PeopleIcon sx={{ fontSize: 48, color: '#1976d2', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Gerenciar Funcionários
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  href="/funcionarios"
                >
                  Acessar
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Card
              sx={{
                height: '100%',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: '0 12px 32px rgba(0, 0, 0, 0.15)'
                }
              }}
            >
              <CardContent sx={{ textAlign: 'center', py: 3 }}>
                <PeopleIcon sx={{ fontSize: 48, color: '#4caf50', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Gerenciar Clientes
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  href="/clientes"
                >
                  Acessar
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Card
              sx={{
                height: '100%',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: '0 12px 32px rgba(0, 0, 0, 0.15)'
                }
              }}
            >
              <CardContent sx={{ textAlign: 'center', py: 3 }}>
                <ShoppingCartIcon sx={{ fontSize: 48, color: '#ff9800', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Gerenciar Produtos
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  href="/produtos"
                >
                  Acessar
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Card
              sx={{
                height: '100%',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: '0 12px 32px rgba(0, 0, 0, 0.15)'
                }
              }}
            >
              <CardContent sx={{ textAlign: 'center', py: 3 }}>
                <ReceiptIcon sx={{ fontSize: 48, color: '#9c27b0', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Gerenciar Comandas
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  href="/comandas"
                >
                  Acessar
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={4}>
            <Card
              sx={{
                height: '100%',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: '0 12px 32px rgba(0, 0, 0, 0.15)'
                }
              }}
            >
              <CardContent sx={{ textAlign: 'center', py: 3 }}>
                <BarChartIcon sx={{ fontSize: 48, color: '#f44336', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Relatório de Caixa
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  href="/caixa"
                >
                  Acessar
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  )
}
