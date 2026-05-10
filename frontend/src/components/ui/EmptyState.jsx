import React from 'react'
import { Box, Typography, Button } from '@mui/material'
import { Inbox as InboxIcon } from '@mui/icons-material'

export const EmptyState = ({ 
  title = 'Nenhum item encontrado', 
  message = 'Não há dados para exibir',
  onAction,
  actionLabel = 'Adicionar'
}) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '400px',
        gap: 2,
        padding: 3
      }}
    >
      <InboxIcon sx={{ fontSize: 80, color: '#ddd' }} />
      <Typography variant="h5" sx={{ fontWeight: 600, color: '#666' }}>
        {title}
      </Typography>
      <Typography variant="body2" sx={{ color: '#999' }}>
        {message}
      </Typography>
      {onAction && (
        <Button variant="contained" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </Box>
  )
}
