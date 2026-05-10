const STORAGE_KEY = 'comandas-do-ze:offline-db'

const defaultDatabase = {
  funcionarios: [
    {
      id: 1,
      nome: 'Ana Souza',
      cpf: '12345678901',
      email: 'ana@comandasdoze.com',
      matricula: 'F001'
    },
    {
      id: 2,
      nome: 'Bruno Lima',
      cpf: '98765432100',
      email: 'bruno@comandasdoze.com',
      matricula: 'F002'
    }
  ],
  clientes: [
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
  ],
  produtos: [
    {
      id: 1,
      nome: 'Cerveja Artesanal',
      descricao: 'Garrafa 600ml gelada',
      preco: 18.9,
      categoria: 'Bebidas',
      estoque: 24
    },
    {
      id: 2,
      nome: 'Porção de Batata',
      descricao: 'Porção grande com cheddar',
      preco: 32.5,
      categoria: 'Petiscos',
      estoque: 12
    }
  ],
  comandas: [
    {
      id: 1,
      numero: 101,
      cliente: 'Carlos Pereira',
      descricao: 'Mesa externa - 4 pessoas',
      valor: 86.4,
      status: 'aberta'
    },
    {
      id: 2,
      numero: 102,
      cliente: 'Mariana Alves',
      descricao: 'Evento aniversário',
      valor: 152.0,
      status: 'paga'
    }
  ],
  nextIds: {
    funcionarios: 3,
    clientes: 3,
    produtos: 3,
    comandas: 3
  }
}

const clone = (value) => JSON.parse(JSON.stringify(value))

const readDatabase = () => {
  if (typeof window === 'undefined') {
    return clone(defaultDatabase)
  }

  const raw = window.localStorage.getItem(STORAGE_KEY)
  if (!raw) {
    const database = clone(defaultDatabase)
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(database))
    return database
  }

  try {
    return JSON.parse(raw)
  } catch {
    const database = clone(defaultDatabase)
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(database))
    return database
  }
}

const writeDatabase = (database) => {
  if (typeof window === 'undefined') {
    return
  }

  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(database))
}

const getNextId = (database, collectionName) => {
  if (!database.nextIds) {
    database.nextIds = {}
  }

  const currentValue = database.nextIds[collectionName]
  if (typeof currentValue === 'number') {
    return currentValue
  }

  const maxExistingId = Math.max(0, ...(database[collectionName] || []).map((item) => Number(item.id) || 0))
  database.nextIds[collectionName] = maxExistingId + 1
  return database.nextIds[collectionName]
}

export const createOfflineCrud = (collectionName, seedRecords) => {
  const ensureCollection = () => {
    const database = readDatabase()
    if (!Array.isArray(database[collectionName]) || database[collectionName].length === 0) {
      database[collectionName] = clone(seedRecords)
      database.nextIds = database.nextIds || {}
      database.nextIds[collectionName] = seedRecords.length + 1
      writeDatabase(database)
    }
    return database
  }

  return {
    getAll() {
      const database = ensureCollection()
      return { success: true, data: clone(database[collectionName]) }
    },

    getById(id) {
      const database = ensureCollection()
      const item = database[collectionName].find((record) => String(record.id) === String(id))
      if (!item) {
        return { success: false, error: 'Registro não encontrado' }
      }
      return { success: true, data: clone(item) }
    },

    create(data) {
      const database = ensureCollection()
      const newRecord = { id: getNextId(database, collectionName), ...data }
      database[collectionName] = [newRecord, ...database[collectionName]]
      database.nextIds[collectionName] = newRecord.id + 1
      writeDatabase(database)
      return { success: true, data: clone(newRecord) }
    },

    update(id, data) {
      const database = ensureCollection()
      const index = database[collectionName].findIndex((record) => String(record.id) === String(id))
      if (index === -1) {
        return { success: false, error: 'Registro não encontrado' }
      }

      const updatedRecord = { ...database[collectionName][index], ...data, id: database[collectionName][index].id }
      database[collectionName][index] = updatedRecord
      writeDatabase(database)
      return { success: true, data: clone(updatedRecord) }
    },

    delete(id) {
      const database = ensureCollection()
      const beforeLength = database[collectionName].length
      database[collectionName] = database[collectionName].filter((record) => String(record.id) !== String(id))
      if (database[collectionName].length === beforeLength) {
        return { success: false, error: 'Registro não encontrado' }
      }
      writeDatabase(database)
      return { success: true }
    }
  }
}

export { defaultDatabase }