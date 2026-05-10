import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm, Controller } from 'react-hook-form'
import {
  Container,
  Box,
  Card,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Typography,
  Paper,
  InputAdornment,
  IconButton
} from '@mui/material'
import { Visibility, VisibilityOff } from '@mui/icons-material'
import { useAuth } from '../../hooks/useAuth'
import { useValidationRules } from '../../hooks/useValidationRules'
import './LoginForm.css'

export const LoginForm = () => {
  const navigate = useNavigate()
  const { login, loading, error } = useAuth()
  const { getRule } = useValidationRules()
  const { control, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      username: '',
      password: ''
    }
  })
  const [showPassword, setShowPassword] = useState(false)

  const onSubmit = async (data) => {
    const result = await login(data.username, data.password)
    if (result.success) {
      navigate('/home')
    }
  }

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh'
        }}
      >
        <Card
          sx={{
            width: '100%',
            padding: 4,
            borderRadius: 2,
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
          }}
        >
          <Box sx={{ textAlign: 'center', marginBottom: 3 }}>
            <Typography
              variant="h3"
              sx={{
                fontWeight: 700,
                background: 'linear-gradient(135deg, #1976d2 0%, #dc004e 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                marginBottom: 1
              }}
            >
              Comandas do Zé
            </Typography>
            <Typography
              variant="body1"
              sx={{
                color: '#666',
                fontWeight: 500
              }}
            >
              Sistema de Gerenciamento
            </Typography>
          </Box>

          <Paper
            sx={{
              padding: 2,
              marginBottom: 2,
              backgroundColor: '#e3f2fd',
              border: '1px solid #90caf9'
            }}
          >
            <Typography variant="caption" sx={{ color: '#1565c0', fontWeight: 600 }}>
              Dados de teste:
            </Typography>
            <Typography variant="caption" sx={{ display: 'block', color: '#1565c0' }}>
              Usuário: <strong>abc</strong>
            </Typography>
            <Typography variant="caption" sx={{ display: 'block', color: '#1565c0' }}>
              Senha: <strong>bolinhas</strong>
            </Typography>
          </Paper>

          {error && (
            <Alert severity="error" sx={{ marginBottom: 2 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit(onSubmit)}>
            <Controller
              name="username"
              control={control}
              rules={{ required: 'Usuário é obrigatório' }}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Usuário"
                  type="text"
                  variant="outlined"
                  margin="normal"
                  error={!!errors.username}
                  helperText={errors.username?.message}
                  disabled={loading}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 1
                    }
                  }}
                />
              )}
            />

            <Controller
              name="password"
              control={control}
              rules={getRule('senha')}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Senha"
                  type={showPassword ? 'text' : 'password'}
                  variant="outlined"
                  margin="normal"
                  error={!!errors.password}
                  helperText={errors.password?.message}
                  disabled={loading}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={() => setShowPassword(!showPassword)}
                          edge="end"
                          disabled={loading}
                        >
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    )
                  }}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 1
                    }
                  }}
                />
              )}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{
                marginTop: 3,
                marginBottom: 2,
                background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
                padding: '12px 24px',
                fontSize: '1rem',
                fontWeight: 600,
                textTransform: 'none',
                position: 'relative'
              }}
            >
              {loading ? (
                <>
                  <CircularProgress
                    size={24}
                    sx={{
                      position: 'absolute',
                      left: '50%',
                      marginLeft: '-12px',
                      color: 'white'
                    }}
                  />
                  Entrando...
                </>
              ) : (
                'Entrar'
              )}
            </Button>
          </form>

          <Typography
            variant="caption"
            sx={{
              display: 'block',
              textAlign: 'center',
              color: '#999',
              marginTop: 2
            }}
          >
            © 2026 Comandas do Zé. Todos os direitos reservados.
          </Typography>
        </Card>
      </Box>
    </Container>
  )
}
