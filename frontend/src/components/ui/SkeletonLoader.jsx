import React from 'react'
import { Skeleton, Box, Stack } from '@mui/material'

export const SkeletonLoader = ({ count = 3 }) => {
  return (
    <Box sx={{ width: '100%' }}>
      <Stack spacing={2}>
        {Array.from({ length: count }).map((_, idx) => (
          <Box key={idx}>
            <Skeleton variant="rectangular" height={60} sx={{ borderRadius: 1 }} />
          </Box>
        ))}
      </Stack>
    </Box>
  )
}
