import React, { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Typography,
  Divider,
  useMediaQuery,
  useTheme,
  Button,
  Menu,
  MenuItem,
  Avatar
} from '@mui/material'
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  Person as PersonIcon,
  ShoppingCart as ShoppingCartIcon,
  Receipt as ReceiptIcon,
  LocalDining as LocalDiningIcon,
  Logout as LogoutIcon,
  Settings as SettingsIcon,
  Close as CloseIcon
} from '@mui/icons-material'
import { useAuth } from '../../hooks/useAuth'

const menuItems = [
  { label: 'Dashboard', icon: DashboardIcon, path: '/home' },
  { label: 'Funcionários', icon: PeopleIcon, path: '/funcionarios' },
  { label: 'Clientes', icon: PersonIcon, path: '/clientes' },
  { label: 'Produtos', icon: ShoppingCartIcon, path: '/produtos' },
  { label: 'Comandas', icon: ReceiptIcon, path: '/comandas' },
  { label: 'Caixa', icon: LocalDiningIcon, path: '/caixa' },
  { label: 'Perfil', icon: PersonIcon, path: '/perfil' }
]

export const Navbar = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { logout, user } = useAuth()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [anchorEl, setAnchorEl] = useState(null)
  const [avatarSrc, setAvatarSrc] = useState('/image.png')

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen)
  }

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
  }

  const handleNavigate = (path) => {
    navigate(path)
    if (isMobile) {
      setDrawerOpen(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
    handleMenuClose()
  }

  const isActive = (path) => location.pathname === path

  const drawerContent = (
    <Box sx={{ width: 280 }}>
      <Box
        sx={{
          padding: 2,
          background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
          color: 'white',
          display: 'flex',
          alignItems: 'center',
          gap: 2
        }}
      >
        <Avatar
          src={avatarSrc}
          alt={user?.username}
          onError={() => setAvatarSrc('/avatar.svg')}
          sx={{
            width: 48,
            height: 48,
            background: 'rgba(255, 255, 255, 0.3)',
            fontSize: '1.5rem',
            border: '2px solid rgba(255, 255, 255, 0.5)',
            cursor: 'pointer'
          }}
        >
          {user?.username?.[0]?.toUpperCase() || 'U'}
        </Avatar>
        <Box>
          <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
            {user?.username || 'Usuário'}
          </Typography>
          <Typography variant="caption">{user?.role || 'Admin'}</Typography>
        </Box>
      </Box>

      <Divider />

      <List>
        {menuItems.map((item) => {
          const Icon = item.icon
          return (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                onClick={() => handleNavigate(item.path)}
                selected={isActive(item.path)}
                sx={{
                  '&.Mui-selected': {
                    backgroundColor: '#e3f2fd',
                    borderLeft: '4px solid #1976d2',
                    paddingLeft: 'calc(1rem - 4px)',
                    '& .MuiListItemIcon-root': {
                      color: '#1976d2'
                    },
                    '& .MuiListItemText-primary': {
                      color: '#1976d2',
                      fontWeight: 600
                    }
                  },
                  '&:hover': {
                    backgroundColor: '#f5f5f5'
                  }
                }}
              >
                <ListItemIcon>
                  <Icon />
                </ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            </ListItem>
          )
        })}
      </List>

      <Divider sx={{ marginTop: 'auto' }} />

      <List>
        <ListItem disablePadding>
          <ListItemButton
            onClick={handleLogout}
            sx={{
              '&:hover': {
                backgroundColor: '#ffebee'
              }
            }}
          >
            <ListItemIcon sx={{ color: '#f44336' }}>
              <LogoutIcon />
            </ListItemIcon>
            <ListItemText
              primary="Logout"
              sx={{
                '& .MuiListItemText-primary': {
                  color: '#f44336'
                }
              }}
            />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  )

  return (
    <>
      <AppBar
        position="sticky"
        sx={{
          background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
          boxShadow: '0 2px 12px rgba(0, 0, 0, 0.15)'
        }}
      >
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ marginRight: 2 }}
            >
              {drawerOpen ? <CloseIcon /> : <MenuIcon />}
            </IconButton>
          )}

          <Typography
            variant="h6"
            sx={{
              fontWeight: 700,
              flexGrow: 1,
              cursor: 'pointer',
              fontSize: { xs: '1.1rem', sm: '1.3rem', md: '1.5rem' }
            }}
            onClick={() => navigate('/home')}
          >
            🍺 Comandas do Zé
          </Typography>

          {!isMobile && (
            <Box sx={{ display: 'flex', gap: 1 }}>
              {menuItems.map((item) => {
                const Icon = item.icon
                return (
                  <Button
                    key={item.path}
                    color="inherit"
                    onClick={() => handleNavigate(item.path)}
                    startIcon={<Icon />}
                    sx={{
                      textTransform: 'none',
                      fontSize: '0.95rem',
                      fontWeight: 500,
                      padding: '8px 12px',
                      borderRadius: 1,
                      backgroundColor: isActive(item.path)
                        ? 'rgba(255, 255, 255, 0.25)'
                        : 'transparent',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.15)'
                      }
                    }}
                  >
                    {item.label}
                  </Button>
                )
              })}
            </Box>
          )}

          <Box sx={{ marginLeft: { xs: 0, md: 2 } }}>
            <IconButton
              color="inherit"
              onClick={handleMenuOpen}
              sx={{
                borderRadius: 1,
                padding: '8px 12px'
              }}
            >
              <Avatar
                src={avatarSrc}
                alt={user?.username}
                onError={() => setAvatarSrc('/avatar.svg')}
                sx={{
                  width: 40,
                  height: 40,
                  background: 'rgba(255, 255, 255, 0.3)',
                  fontSize: '1rem',
                  cursor: 'pointer',
                  border: '2px solid rgba(255, 255, 255, 0.5)',
                  '&:hover': {
                    transform: 'scale(1.05)',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
                  },
                  transition: 'all 0.3s ease'
                }}
              >
                {user?.username?.[0]?.toUpperCase() || 'U'}
              </Avatar>
            </IconButton>

            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right'
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right'
              }}
            >
              <MenuItem disabled>
                <Typography variant="body2" sx={{ fontWeight: 600 }}>
                  {user?.username}
                </Typography>
              </MenuItem>
              <Divider />
              <MenuItem
                onClick={() => {
                  handleNavigate('/perfil')
                  handleMenuClose()
                }}
              >
                <PersonIcon sx={{ marginRight: 1 }} />
                Meu Perfil
              </MenuItem>
              <MenuItem>
                <SettingsIcon sx={{ marginRight: 1 }} />
                Configurações
              </MenuItem>
              <Divider />
              <MenuItem onClick={handleLogout}>
                <LogoutIcon sx={{ marginRight: 1, color: '#f44336' }} />
                <Typography sx={{ color: '#f44336' }}>Sair</Typography>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>

      {isMobile && (
        <Drawer
          anchor="left"
          open={drawerOpen}
          onClose={handleDrawerToggle}
          variant="temporary"
        >
          {drawerContent}
        </Drawer>
      )}
    </>
  )
}
