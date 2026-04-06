import os

from dotenv import load_dotenv


load_dotenv()

# Configuracoes da API
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
RELOAD = os.getenv("RELOAD", "true").lower() == "true"

# Configuracoes de rate limiting
RATE_LIMIT_DEFAULT = os.getenv("RATE_LIMIT_DEFAULT", "120/minute")
RATE_LIMIT_LOW = os.getenv("RATE_LIMIT_LOW", "60/minute")
RATE_LIMIT_MODERATE = os.getenv("RATE_LIMIT_MODERATE", "30/minute")
RATE_LIMIT_RESTRICTIVE = os.getenv("RATE_LIMIT_RESTRICTIVE", "10/minute")
RATE_LIMIT_CRITICAL = os.getenv("RATE_LIMIT_CRITICAL", "5/minute")

# Configuracoes de autenticacao
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_this_secret_in_production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Credenciais do usuario admin bootstrap
BOOTSTRAP_ADMIN_NOME = os.getenv("BOOTSTRAP_ADMIN_NOME", "Administrador")
BOOTSTRAP_ADMIN_MATRICULA = os.getenv("BOOTSTRAP_ADMIN_MATRICULA", "admin")
BOOTSTRAP_ADMIN_CPF = os.getenv("BOOTSTRAP_ADMIN_CPF", "00000000000")
BOOTSTRAP_ADMIN_TELEFONE = os.getenv("BOOTSTRAP_ADMIN_TELEFONE", "11999999999")
BOOTSTRAP_ADMIN_GRUPO = os.getenv("BOOTSTRAP_ADMIN_GRUPO", "1")
BOOTSTRAP_ADMIN_SENHA = os.getenv("BOOTSTRAP_ADMIN_SENHA", "admin123")

# Configuracoes do banco
DB_DIALECT = os.getenv("DB_DIALECT", "sqlite")
DB_NAME = os.getenv("DB_NAME", "comanda.db")

# Configuracoes de health check (percentual)
HEALTH_WARN_CPU_PERCENT = float(os.getenv("HEALTH_WARN_CPU_PERCENT", "80"))
HEALTH_FAIL_CPU_PERCENT = float(os.getenv("HEALTH_FAIL_CPU_PERCENT", "90"))
HEALTH_WARN_MEMORY_PERCENT = float(os.getenv("HEALTH_WARN_MEMORY_PERCENT", "80"))
HEALTH_FAIL_MEMORY_PERCENT = float(os.getenv("HEALTH_FAIL_MEMORY_PERCENT", "90"))
HEALTH_WARN_DISK_PERCENT = float(os.getenv("HEALTH_WARN_DISK_PERCENT", "85"))
HEALTH_FAIL_DISK_PERCENT = float(os.getenv("HEALTH_FAIL_DISK_PERCENT", "95"))

if DB_DIALECT == "sqlite":
	STR_DATABASE = f"sqlite:///./{DB_NAME}"
else:
	DB_USER = os.getenv("DB_USER", "")
	DB_PASSWORD = os.getenv("DB_PASSWORD", "")
	DB_HOST = os.getenv("DB_HOST", "")
	DB_PORT = os.getenv("DB_PORT", "")
	STR_DATABASE = (
		f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
	)