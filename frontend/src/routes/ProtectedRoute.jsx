import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { NotFoundPage } from '../pages/NotFoundPage'

const protectedRoutes = [
  '/home',
  '/funcionarios',
  '/clientes',
  '/produtos',
  '/comandas',
  '/caixa',
  '/perfil'
]

export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth()
  const location = useLocation()

  const isProtectedPath = protectedRoutes.includes(location.pathname)

  if (!isProtectedPath) {
    return <NotFoundPage />
  }

  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />
  }

  return children
}
