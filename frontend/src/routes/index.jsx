import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { LoginForm } from '../components/forms/LoginForm'
import { ProtectedRoute } from './ProtectedRoute'
import { Home } from '../pages/Home'
import { FuncionariosPage } from '../pages/FuncionariosPage'
import { ClientesPage } from '../pages/ClientesPage'
import { ProdutosPage } from '../pages/ProdutosPage'
import { ComandasPage } from '../pages/ComandasPage'
import { CaixaPage } from '../pages/CaixaPage'
import { PerfilPage } from '../pages/PerfilPage'
import { NotFoundPage } from '../pages/NotFoundPage'
import { Navbar } from '../components/common/Navbar'
import { Box } from '@mui/material'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm />} />

      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
              <Navbar />
              <Box component="main" sx={{ flex: 1, padding: { xs: 2, sm: 3 } }}>
                <Routes>
                  <Route path="/home" element={<Home />} />
                  <Route path="/funcionarios" element={<FuncionariosPage />} />
                  <Route path="/clientes" element={<ClientesPage />} />
                  <Route path="/produtos" element={<ProdutosPage />} />
                  <Route path="/comandas" element={<ComandasPage />} />
                  <Route path="/caixa" element={<CaixaPage />} />
                  <Route path="/perfil" element={<PerfilPage />} />
                  <Route path="*" element={<NotFoundPage />} />
                </Routes>
              </Box>
            </Box>
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}
