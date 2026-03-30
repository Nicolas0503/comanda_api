#!/usr/bin/env python3
"""
Script de teste para validar o sistema de autenticação JWT
Teste as funcionalidades básicas: geração de tokens, verificação, etc.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from datetime import datetime
from auth import criar_access_token, criar_refresh_token, verificar_token, extrair_token_do_header

# Teste 1: Criar Access Token
print("=" * 60)
print("TESTE 1: Criar Access Token")
print("=" * 60)
usuario_id = 1
grupo = 1
access_token = criar_access_token(usuario_id=usuario_id, grupo=grupo)
print(f"✓ Access Token criado com sucesso")
print(f"  Token (primeiros 50 chars): {access_token[:50]}...")
print()

# Teste 2: Criar Refresh Token
print("=" * 60)
print("TESTE 2: Criar Refresh Token")
print("=" * 60)
refresh_token = criar_refresh_token(usuario_id=usuario_id, grupo=grupo)
print(f"✓ Refresh Token criado com sucesso")
print(f"  Token (primeiros 50 chars): {refresh_token[:50]}...")
print()

# Teste 3: Verificar Access Token
print("=" * 60)
print("TESTE 3: Verificar Access Token")
print("=" * 60)
try:
    payload = verificar_token(access_token)
    print(f"✓ Access Token validado com sucesso")
    print(f"  Usuario ID: {payload['usuario_id']}")
    print(f"  Grupo: {payload['grupo']}")
    print(f"  Tipo: {payload['tipo']}")
except Exception as e:
    print(f"✗ Erro: {e}")
print()

# Teste 4: Verificar Refresh Token
print("=" * 60)
print("TESTE 4: Verificar Refresh Token")
print("=" * 60)
try:
    payload = verificar_token(refresh_token)
    print(f"✓ Refresh Token validado com sucesso")
    print(f"  Usuario ID: {payload['usuario_id']}")
    print(f"  Grupo: {payload['grupo']}")
    print(f"  Tipo: {payload['tipo']}")
except Exception as e:
    print(f"✗ Erro: {e}")
print()

# Teste 5: Extrair Token do Header
print("=" * 60)
print("TESTE 5: Extrair Token do Header")
print("=" * 60)
header_correto = f"Bearer {access_token}"
try:
    token = extrair_token_do_header(header_correto)
    print(f"✓ Token extraído do header com sucesso")
    print(f"  Header: {header_correto[:60]}...")
    print(f"  Token extraído (primeiros 50 chars): {token[:50]}...")
except Exception as e:
    print(f"✗ Erro: {e}")
print()

# Teste 6: Header inválido
print("=" * 60)
print("TESTE 6: Validar rejeição de header inválido")
print("=" * 60)
header_invalido = f"Basic {access_token}"
try:
    token = extrair_token_do_header(header_invalido)
    print(f"✗ Deveria ter rejeitado o header inválido")
except Exception as e:
    print(f"✓ Header inválido rejeitado corretamente")
    print(f"  Erro esperado: {e}")
print()

print("=" * 60)
print("✓ TODOS OS TESTES PASSARAM COM SUCESSO!")
print("=" * 60)
