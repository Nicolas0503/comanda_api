import React from 'react'
import {
  Card,
  CardContent,
  Typography,
  Box,
  Stack
} from '@mui/material'

export const StatCard = ({ 
  title, 
  value, 
  icon: Icon, 
  color = 'primary',
  trend,
  trendDirection = 'up'
}) => {
  return (
    <Card
      sx={{
        height: '100%',
        background: `linear-gradient(135deg, ${color}20 0%, ${color}10 100%)`,
        border: `1px solid ${color}30`,
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: `0 8px 24px ${color}40`
        }
      }}
    >
      <CardContent>
        <Stack spacing={2} sx={{ height: '100%' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <Box>
              <Typography 
                variant="caption" 
                sx={{ 
                  color: '#666', 
                  fontWeight: 600,
                  textTransform: 'uppercase',
                  letterSpacing: 0.5
                }}
              >
                {title}
              </Typography>
            </Box>
            {Icon && (
              <Icon 
                sx={{ 
                  color: color === 'primary' ? '#1976d2' : color,
                  fontSize: 28
                }} 
              />
            )}
          </Box>

          <Typography 
            variant="h4" 
            sx={{ 
              fontWeight: 700,
              color: color === 'primary' ? '#1976d2' : color
            }}
          >
            {value}
          </Typography>

          {trend && (
            <Typography 
              variant="caption" 
              sx={{
                color: trendDirection === 'up' ? '#4caf50' : '#f44336',
                fontWeight: 600
              }}
            >
              {trendDirection === 'up' ? '↑' : '↓'} {trend}
            </Typography>
          )}
        </Stack>
      </CardContent>
    </Card>
  )
}
