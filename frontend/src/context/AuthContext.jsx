import React, { createContext, useState, useCallback, useEffect } from 'react'

export const AuthContext = createContext()

const MOCK_USERS = {
  abc: 'bolinhas'
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Verificar autenticação ao montar o componente
  useEffect(() => {
    const storedUser = sessionStorage.getItem('user')
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch (e) {
        sessionStorage.removeItem('user')
      }
    }
  }, [])

  const login = useCallback(async (username, password) => {
    setLoading(true)
    setError(null)

    try {
      // Simular delay de requisição
      await new Promise(resolve => setTimeout(resolve, 500))

      if (MOCK_USERS[username] && MOCK_USERS[username] === password) {
        const userData = {
          username,
          email: `${username}@comandas.com`,
          role: 'admin',
          loginTime: new Date().toISOString()
        }
        setUser(userData)
        sessionStorage.setItem('user', JSON.stringify(userData))
        return { success: true, user: userData }
      } else {
        const error = 'Usuário ou senha inválidos'
        setError(error)
        return { success: false, error }
      }
    } catch (err) {
      const errorMsg = 'Erro ao fazer login'
      setError(errorMsg)
      return { success: false, error: errorMsg }
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(() => {
    setUser(null)
    sessionStorage.removeItem('user')
    setError(null)
  }, [])

  const isAuthenticated = useCallback(() => {
    return user !== null
  }, [user])

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
