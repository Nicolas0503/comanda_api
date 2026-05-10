import { useState, useCallback } from 'react'

export const useSnackbar = () => {
  const [open, setOpen] = useState(false)
  const [message, setMessage] = useState('')
  const [severity, setSeverity] = useState('success')

  const showSnackbar = useCallback((msg, type = 'success') => {
    setMessage(msg)
    setSeverity(type)
    setOpen(true)
  }, [])

  const closeSnackbar = useCallback(() => {
    setOpen(false)
  }, [])

  return {
    open,
    message,
    severity,
    showSnackbar,
    closeSnackbar
  }
}
