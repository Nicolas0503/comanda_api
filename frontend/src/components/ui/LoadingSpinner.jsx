import React from 'react'
import { CircularProgress, Box, Typography } from '@mui/material'

export const LoadingSpinner = ({ message = 'Carregando...' }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '400px',
        gap: 2
      }}
    >
      <CircularProgress size={60} />
      <Typography variant="body1" sx={{ color: '#666' }}>
        {message}
      </Typography>
    </Box>
  )
}
