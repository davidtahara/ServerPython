import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from os import listdir
from os.path import isfile, join

# Carrega as variáveis de ambiente
load_dotenv()

# Variáveis de ambiente
porta = int(os.getenv("PORT", 3001))  # Valor padrão definido para 3001 caso PORT não esteja configurada

# Inicializa o FastAPI
app = FastAPI()

# Adiciona o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importa e inclui os routers dos módulos
modules_path = "Modules"
modules = [f for f in listdir(modules_path) if not isfile(join(modules_path, f))]
for module in modules:
    routers_path = f"{modules_path}/{module}/routers"
    if not os.path.exists(routers_path):
        continue  # Pule se a pasta de routers não existir
    files = [f for f in listdir(routers_path) if f.endswith(".py") and f != "__init__.py"]
    for file in files:
        try:
            module_name = f"Modules.{module}.routers.{file[:-3]}"
            router = __import__(module_name, fromlist=["router"]).router
            app.include_router(router)
            print(f"Successfully included router from {module_name}")
        except Exception as e:
            print(f"Failed to include router from {module_name}: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=porta)
