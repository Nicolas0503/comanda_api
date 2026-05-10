import React, { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import {
  Container,
  Box,
  Card,
  CardContent,
  Typography,
  Avatar,
  Button,
  Grid,
  Paper,
  Stack,
  Chip
} from '@mui/material'
import {
  Edit as EditIcon,
  Email as EmailIcon,
  Person as PersonIcon,
  Security as SecurityIcon
} from '@mui/icons-material'

export const PerfilPage = () => {
  const { user, logout } = useAuth()
  const [avatarSrc, setAvatarSrc] = useState('/image.png')

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      {/* Header Card com Avatar Destaque */}
      <Card
        sx={{
          background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
          color: 'white',
          marginBottom: 4,
          borderRadius: 3,
          overflow: 'hidden',
          boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)'
        }}
      >
        <CardContent sx={{ textAlign: 'center', py: 4 }}>
          {/* Avatar Grande com Imagem */}
          <Box sx={{ marginBottom: 3, display: 'flex', justifyContent: 'center' }}>
            <Avatar
              src={avatarSrc}
              alt={user?.username}
              onError={() => setAvatarSrc('/avatar.svg')}
              sx={{
                width: 150,
                height: 150,
                fontSize: '4rem',
                background: 'rgba(255, 255, 255, 0.25)',
                border: '4px solid rgba(255, 255, 255, 0.5)',
                boxShadow: '0 8px 16px rgba(0, 0, 0, 0.2)'
              }}
            >
              {user?.username?.[0]?.toUpperCase()}
            </Avatar>
          </Box>

          <Typography variant="h4" sx={{ fontWeight: 700, marginBottom: 1 }}>
            {user?.username || 'Usuário'}
          </Typography>

          <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center', mb: 2 }}>
            <Chip
              label={user?.role || 'Admin'}
              sx={{
                backgroundColor: 'rgba(255, 255, 255, 0.25)',
                color: 'white',
                fontWeight: 600
              }}
            />
            <Chip
              label="Autenticado"
              variant="outlined"
              sx={{
                borderColor: 'rgba(255, 255, 255, 0.5)',
                color: 'white',
                fontWeight: 600
              }}
            />
          </Box>

          <Typography variant="body1" sx={{ opacity: 0.9, mb: 3 }}>
            Bem-vindo à sua página de perfil
          </Typography>

          <Stack direction="row" spacing={2} justifyContent="center" sx={{ flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              startIcon={<EditIcon />}
              sx={{
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.35)'
                }
              }}
            >
              Editar Perfil
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {/* Informações */}
      <Grid container spacing={3} sx={{ marginBottom: 4 }}>
        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 3,
              borderRadius: 2,
              background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.1) 0%, rgba(21, 101, 192, 0.1) 100%)',
              border: '1px solid #e3f2fd'
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <PersonIcon sx={{ color: '#1976d2', fontSize: '2rem' }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Nome de Usuário
              </Typography>
            </Box>
            <Typography variant="body2" sx={{ color: '#555', ml: 7 }}>
              {user?.username || 'Não informado'}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 3,
              borderRadius: 2,
              background: 'linear-gradient(135deg, rgba(220, 0, 78, 0.1) 0%, rgba(194, 24, 91, 0.1) 100%)',
              border: '1px solid #fce4ec'
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <SecurityIcon sx={{ color: '#dc004e', fontSize: '2rem' }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Nível de Acesso
              </Typography>
            </Box>
            <Typography variant="body2" sx={{ color: '#555', ml: 7 }}>
              {user?.role || 'Administrador'}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper
            sx={{
              p: 3,
              borderRadius: 2,
              background: 'linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(56, 142, 60, 0.1) 100%)',
              border: '1px solid #e8f5e9'
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <EmailIcon sx={{ color: '#4caf50', fontSize: '2rem' }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Status
              </Typography>
            </Box>
            <Typography variant="body2" sx={{ color: '#555', ml: 7 }}>
              ✅ Conectado e Autenticado
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Seção de Ações */}
      <Card
        sx={{
          borderRadius: 2,
          border: '1px solid #e0e0e0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)'
        }}
      >
        <CardContent>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
            Ações
          </Typography>

          <Stack spacing={2}>
            <Button
              fullWidth
              variant="outlined"
              sx={{
                borderColor: '#1976d2',
                color: '#1976d2',
                '&:hover': {
                  backgroundColor: '#f5f5f5',
                  borderColor: '#1565c0'
                }
              }}
            >
              Alterar Senha
            </Button>

            <Button
              fullWidth
              variant="outlined"
              sx={{
                borderColor: '#dc004e',
                color: '#dc004e',
                '&:hover': {
                  backgroundColor: '#fef5f5',
                  borderColor: '#c2185b'
                }
              }}
            >
              Preferências
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {/* Rodapé com Logout */}
      <Box sx={{ textAlign: 'center', mt: 6 }}>
        <Typography variant="body2" sx={{ color: '#999', mb: 2 }}>
          Última atualização: {new Date().toLocaleDateString('pt-BR')}
        </Typography>
      </Box>
    </Container>
  )
}
