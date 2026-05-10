import api from './api'
import { createOfflineCrud } from './offlineStore'

const ENDPOINT = '/clientes'
const offline = createOfflineCrud('clientes', [
  {
    id: 1,
    nome: 'Carlos Pereira',
    cpf: '11122233344',
    email: 'carlos@email.com',
    telefone: '11999999999',
    endereco: 'Rua das Flores, 123',
    cidade: 'São Paulo',
    estado: 'SP'
  },
  {
    id: 2,
    nome: 'Mariana Alves',
    cpf: '55566677788',
    email: 'mariana@email.com',
    telefone: '11988887777',
    endereco: 'Avenida Central, 450',
    cidade: 'Osasco',
    estado: 'SP'
  }
])

const isNetworkError = (error) => !error.response || error.code === 'ERR_NETWORK' || /Network Error/i.test(error.message)

export const clientesService = {
  async getAll() {
    try {
      const response = await api.get(ENDPOINT)
      return { success: true, data: response.data }
    } catch (error) {
      return isNetworkError(error) ? offline.getAll() : { success: false, error: error.message }
    }
  },

  async getById(id) {
    try {
      const response = await api.get(`${ENDPOINT}/${id}`)
      return { success: true, data: response.data }
    } catch (error) {
      return isNetworkError(error) ? offline.getById(id) : { success: false, error: error.message }
    }
  },

  async create(data) {
    try {
      const response = await api.post(ENDPOINT, data)
      return { success: true, data: response.data }
    } catch (error) {
      return isNetworkError(error)
        ? offline.create(data)
        : { success: false, error: error.response?.data?.detail || error.message }
    }
  },

  async update(id, data) {
    try {
      const response = await api.put(`${ENDPOINT}/${id}`, data)
      return { success: true, data: response.data }
    } catch (error) {
      return isNetworkError(error)
        ? offline.update(id, data)
        : { success: false, error: error.response?.data?.detail || error.message }
    }
  },

  async delete(id) {
    try {
      await api.delete(`${ENDPOINT}/${id}`)
      return { success: true }
    } catch (error) {
      return isNetworkError(error) ? offline.delete(id) : { success: false, error: error.message }
    }
  }
}
