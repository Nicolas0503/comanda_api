import api from './api'
import { createOfflineCrud } from './offlineStore'

const ENDPOINT = '/produtos'
const offline = createOfflineCrud('produtos', [
  { id: 1, nome: 'Cerveja Artesanal', descricao: 'Garrafa 600ml gelada', preco: 18.9, categoria: 'Bebidas', estoque: 24 },
  { id: 2, nome: 'Porção de Batata', descricao: 'Porção grande com cheddar', preco: 32.5, categoria: 'Petiscos', estoque: 12 }
])

const isNetworkError = (error) => !error.response || error.code === 'ERR_NETWORK' || /Network Error/i.test(error.message)

export const produtosService = {
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
