import api from './api'
import { createOfflineCrud } from './offlineStore'

const ENDPOINT = '/comandas'
const offline = createOfflineCrud('comandas', [
  { id: 1, numero: 101, cliente: 'Carlos Pereira', descricao: 'Mesa externa - 4 pessoas', valor: 86.4, status: 'aberta' },
  { id: 2, numero: 102, cliente: 'Mariana Alves', descricao: 'Evento aniversário', valor: 152.0, status: 'paga' }
])

const isNetworkError = (error) => !error.response || error.code === 'ERR_NETWORK' || /Network Error/i.test(error.message)

export const comandasService = {
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
