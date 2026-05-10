export const useValidationRules = () => {
  const rules = {
    nome: {
      required: 'Nome é obrigatório',
      minLength: {
        value: 3,
        message: 'Nome deve ter no mínimo 3 caracteres'
      },
      pattern: {
        value: /^[a-zA-ZÀ-ÿ\s]*$/,
        message: 'Nome deve conter apenas letras'
      }
    },
    cpf: {
      required: 'CPF é obrigatório',
      pattern: {
        value: /^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$/,
        message: 'CPF deve estar no formato válido (###.###.###-##)'
      }
    },
    email: {
      required: 'Email é obrigatório',
      pattern: {
        value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        message: 'Email inválido'
      }
    },
    senha: {
      required: 'Senha é obrigatória',
      minLength: {
        value: 6,
        message: 'Senha deve ter no mínimo 6 caracteres'
      }
    },
    matricula: {
      required: 'Matrícula é obrigatória',
      minLength: {
        value: 3,
        message: 'Matrícula deve ter no mínimo 3 caracteres'
      }
    },
    valor: {
      required: 'Valor é obrigatório',
      min: {
        value: 0.01,
        message: 'Valor deve ser maior que 0'
      },
      pattern: {
        value: /^\d+(\.\d{1,2})?$/,
        message: 'Valor deve ser um número válido'
      }
    },
    descricao: {
      minLength: {
        value: 3,
        message: 'Descrição deve ter no mínimo 3 caracteres'
      }
    },
    categoria: {
      required: 'Categoria é obrigatória'
    },
    status: {
      required: 'Status é obrigatório'
    },
    telefone: {
      pattern: {
        value: /^\(\d{2}\)\s\d{4,5}-\d{4}$|^\d{10,11}$/,
        message: 'Telefone inválido'
      }
    },
    endereco: {
      minLength: {
        value: 5,
        message: 'Endereço deve ter no mínimo 5 caracteres'
      }
    },
    cidade: {
      required: 'Cidade é obrigatória',
      minLength: {
        value: 3,
        message: 'Cidade deve ter no mínimo 3 caracteres'
      }
    },
    estado: {
      required: 'Estado é obrigatório'
    }
  }

  const getRule = (field) => {
    return rules[field] || {}
  }

  const getAllRules = () => {
    return rules
  }

  return {
    getRule,
    getAllRules
  }
}
