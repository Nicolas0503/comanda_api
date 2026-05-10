import React from 'react'
import { Card, CardContent, Box, Skeleton, Stack } from '@mui/material'

export const SkeletonCard = ({ count = 4 }) => {
  return (
    <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: '1fr 1fr 1fr 1fr' }, gap: 2 }}>
      {Array.from({ length: count }).map((_, idx) => (
        <Card key={idx}>
          <CardContent>
            <Stack spacing={2}>
              <Skeleton variant="text" width="80%" />
              <Skeleton variant="rectangular" height={80} />
              <Skeleton variant="text" width="60%" />
            </Stack>
          </CardContent>
        </Card>
      ))}
    </Box>
  )
}
