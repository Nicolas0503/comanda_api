import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Box, Card, CardContent, Container, Typography, Button } from '@mui/material'
import { ErrorOutline as ErrorOutlineIcon, Home as HomeIcon } from '@mui/icons-material'

export const NotFoundPage = () => {
  const navigate = useNavigate()

  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Card
        sx={{
          borderRadius: 4,
          overflow: 'hidden',
          boxShadow: '0 16px 40px rgba(0, 0, 0, 0.12)',
          background: 'linear-gradient(135deg, rgba(25,118,210,0.12) 0%, rgba(220,0,78,0.10) 100%)'
        }}
      >
        <CardContent sx={{ textAlign: 'center', py: 8 }}>
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
            <ErrorOutlineIcon sx={{ fontSize: 100, color: '#1976d2' }} />
          </Box>

          <Typography variant="h2" sx={{ fontWeight: 800, mb: 1, color: '#1f1f1f' }}>
            404
          </Typography>

          <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
            Página não encontrada
          </Typography>

          <Typography variant="body1" sx={{ color: '#666', maxWidth: 560, mx: 'auto', mb: 4 }}>
            A rota acessada não existe nesta aplicação. Use essa tela no vídeo para mostrar a
            validação de rotas inexistentes.
          </Typography>

          <Button
            variant="contained"
            startIcon={<HomeIcon />}
            onClick={() => navigate('/home')}
            sx={{
              px: 4,
              py: 1.2,
              borderRadius: 999,
              background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)'
            }}
          >
            Voltar para Home
          </Button>
        </CardContent>
      </Card>
    </Container>
  )
}